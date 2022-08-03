from pydantic import BaseModel


class Order(BaseModel):

    globalId: int
    order_date: str
    delivery_type: str
    client_logo: str
    client_name: str
    client_full_name: str
    detail_num: str
    detail_label: str
    sum_value: int
    sum_profit: int
    return_data: str
    return_data_shipping: str
    status_shipping: str
    arrival_date: str

    class Config:
        orm_mode = True
