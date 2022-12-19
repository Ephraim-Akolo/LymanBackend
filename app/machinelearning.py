from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from . import models as db_models
import numpy as np
from numpy.linalg import norm as np_norm
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import norm as scipy_norm


def cosine_similarity(product:np.ndarray, products:csr_matrix):
    '''
    Finds the cosine similarity between a vector and an array of vectors
    :param
    product: a vector
    products: an array of vectors (2D)
    '''
    return products.dot(product)/(scipy_norm(products, axis=1)*np_norm(product))

def predictor(customer_id:int, db_session:Session, num_recommendations:int=10):
    # get the order ids of the recent transaction that has been rated and also of the client that just placed an order
    purchases = db_session.query(db_models.Purchase).with_entities(db_models.Purchase.order_id, db_models.Purchase.rating, db_models.Purchase.artistan_id) \
        .filter(db_models.Purchase.artistan_id > 0).order_by(db_models.Purchase.order_id.asc()).limit(10**5).all()
    purchases = np.array(purchases)
    last_purchase = db_session.query(db_models.Purchase).with_entities(db_models.Purchase.order_id).filter(db_models.Purchase.customer_id==customer_id).order_by(db_models.Purchase.created_at.desc()).limit(1).first()
    if last_purchase is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record of order found!")
    last_purchase = last_purchase[0]
    # get the products ids of the previous orders and customer recent order
    last_order = db_session.query(db_models.Order).filter(db_models.Order.order_id==last_purchase).with_entities(db_models.Order.product_id).all()
    prev_orders = db_session.query(db_models.Order).with_entities(db_models.Order.order_id, db_models.Order.product_id).filter(db_models.Order.order_id.in_(purchases[:, 0])).order_by(db_models.Order.order_id.asc()).all()
    product_table_max_id = db_session.query(db_models.Product).with_entities(db_models.Product.id).order_by(db_models.Product.id.desc()).limit(1).first()
    product_table_max_id = product_table_max_id[0] + 1
    
    prev_orders = np.array(prev_orders)

    # create the boolean vector from product id
    last_order_vector = np.zeros(product_table_max_id)
    last_order_vector[np.array(last_order)[:, 0]-1] = 1
    
    # adjust the table to start from zero for products ids and order ids
    prev_orders[:, 1] -= 1
    j = 0
    _l = len(prev_orders)-1
    for i in range(len(np.unique(prev_orders[:, 0]))):
        while prev_orders[j, 0] == prev_orders[j+1, 0]:
            prev_orders[j, 0] = i
            j += 1
            if j == _l:
                prev_orders[j, 0] = i
                break
        else:
            prev_orders[j, 0] = i
            j += 1
    max_order_id = i
    # create a sparse matrix order X product
    product_orders_matrix = csr_matrix((np.ones(len(prev_orders)), (prev_orders[:, 0], prev_orders[:, 1])), shape=(max_order_id+1, product_table_max_id))
    similarities = cosine_similarity(last_order_vector, product_orders_matrix)

    # unique_order_ids = np.unique(prev_orders[:, 0])
    # unique_order_ids += min_order_id
    
    # fetch the top highest similar
    order_ranking = np.argsort(similarities)[::-1]

    recommended_orders = purchases[order_ranking]

    rating_ranking = np.argsort(recommended_orders[:, 1])[::-1]
    recommended_artistans = recommended_orders[rating_ranking, 2]
    recommended_artistans = recommended_artistans[np.sort(np.unique(recommended_artistans, return_index=True)[1])][:num_recommendations].tolist()

    artistans = db_session.query(db_models.Artistan).filter(db_models.Artistan.id.in_(recommended_artistans)).all()
    _artistan_len = len(artistans)
    
    sorted_artistans = [i for i in range(_artistan_len)]
    for a in artistans:
        sorted_artistans[recommended_artistans.index(a.id)] = a
    if _artistan_len < num_recommendations:
        extra_artistans = db_session.query(db_models.Artistan).filter(~db_models.Artistan.id.in_(recommended_artistans)).limit(num_recommendations-_artistan_len).all()
        return sorted_artistans + extra_artistans
    return sorted_artistans
    

    