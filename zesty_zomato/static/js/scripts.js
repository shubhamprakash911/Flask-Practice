$(document).ready(function() {
    // Fetch and display the menu
    $.ajax({
        url: '/menu',
        type: 'GET',
        success: function(data) {
            var menuContainer = $('#menu-container');

            // Iterate over each dish in the menu
            $.each(data, function(_, dish) {
                var card = $('<div class="card"></div>');
                var cardBody = $('<div class="card-body"></div>');

                var dishName = $('<h5 class="card-title"></h5>').text(dish.dish_name);
                var dishPrice = $('<p class="card-text"></p>').text('Price: $' + dish.price);
                var dishAvailability = $('<p class="card-text"></p>').text('Availability: ' + (dish.availability ? 'Yes' : 'No'));

                cardBody.append(dishName, dishPrice, dishAvailability);
                card.append(cardBody);
                menuContainer.append(card);
            });
        },
        error: function() {
            alert('Error fetching menu. Please try again.');
        }
    });

    // Fetch and display the orders
    $.ajax({
        url: '/orders',
        type: 'GET',
        success: function(data) {
            var ordersContainer = $('#orders-container');

            // Iterate over each order
            $.each(data, function(_, order) {
                var card = $('<div class="card"></div>');
                var cardBody = $('<div class="card-body"></div>');

                var orderId = $('<h5 class="card-title"></h5>').text('Order ID: ' + order.order_id);
                var customerName = $('<p class="card-text"></p>').text('Customer: ' + order.customer_name);
                var dishIds = $('<p class="card-text"></p>').text('Dish IDs: ' + order.dish_ids.join(', '));
                var orderStatus = $('<p class="card-text"></p>').text('Status: ' + order.status);

                cardBody.append(orderId, customerName, dishIds, orderStatus);
                card.append(cardBody);
                ordersContainer.append(card);
            });
        },
        error: function() {
            alert('Error fetching orders. Please try again.');
        }
    });
});
