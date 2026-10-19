select order_date, count(*) as orders
from {{ ref('orders') }}
group by order_date
