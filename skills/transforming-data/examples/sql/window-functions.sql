-- Advanced SQL Window Functions Examples

-- 1. Moving averages and cumulative sums
with daily_sales as (
    select
        date_trunc('day', order_created_at) as order_date,
        region,
        sum(total_revenue) as daily_revenue
    from fct_orders
    group by 1, 2
),

with_window_calcs as (
    select
        order_date,
        region,
        daily_revenue,

        -- 7-day moving average
        avg(daily_revenue) over (
            partition by region
            order by order_date
            rows between 6 preceding and current row
        ) as revenue_7d_ma,

        -- Cumulative sum (month-to-date)
        sum(daily_revenue) over (
            partition by region, date_trunc('month', order_date)
            order by order_date
        ) as revenue_mtd,

        -- Rank within region
        row_number() over (
            partition by region
            order by daily_revenue desc
        ) as revenue_rank

    from daily_sales
)

select * from with_window_calcs;

-- 2. LAG and LEAD for period-over-period comparisons
select
    order_date,
    revenue,
    lag(revenue, 1) over (order by order_date) as prev_day_revenue,
    lead(revenue, 1) over (order by order_date) as next_day_revenue,
    revenue - lag(revenue, 1) over (order by order_date) as day_over_day_change,
    ((revenue / lag(revenue, 1) over (order by order_date)) - 1) * 100 as pct_change
from daily_sales;

-- 3. Customer order sequencing
select
    customer_id,
    order_id,
    order_date,
    order_amount,
    row_number() over (partition by customer_id order by order_date) as order_number,
    sum(order_amount) over (
        partition by customer_id
        order by order_date
    ) as customer_lifetime_value
from fct_orders;
