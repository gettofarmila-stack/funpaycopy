from enum import Enum


class OrderStatus(str, Enum):
    REFUNDED = 'refunded'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'