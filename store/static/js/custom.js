$(document).ready(function () {
    $(document).on('click', '.increment-btn', function (e) {
        e.preventDefault();

        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value, 10);
        value = isNaN(value) ? 0 : value;
        var maxValue = parseInt($(this).closest('.product_data').find('.qty-input').attr('max'), 10);
        maxValue = isNaN(maxValue) ? 10 : maxValue;

        if (value < maxValue) {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $(document).on('click', '.decrement-btn', function (e) {
        e.preventDefault();

        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value, 10);
        value = isNaN(value) ? 0 : value;
        if (value > 1) {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $(document).on('click', '.Addtocartbtn', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            }
        });
    });

    //ChangeQuantity
    $(document).on('click', '.update-cart-btn', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var product_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id': product_id,
                'product_qty': product_qty,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
                $('.cartdata').load(location.href + " .cartdata");
            }
        });
    });

    //delete-cart-item
    $(document).on('click', '.delete-cart-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
                $('.cartdata').load(location.href + " .cartdata");
            }
        });
    });

    //add-to-wishlist
    $(document).on('click', '.addtowishlist', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
            }
        });
    });

    //delete-wishlist
    $(document).on('click', '.delete-wishlist-item', function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/delete-wishlist-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                console.log(response);
                alertify.success(response.status);
                $('.wishdata').load(location.href + " .wishdata");
            }
        });
    });

    //move to cart from wishlist
    $(document).on('click', '.move-to-cart', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id': product_id,
                'product_qty': 1,
                csrfmiddlewaretoken: token
            },
            success: function () {
                $.ajax({
                    method: "POST",
                    url: "/delete-wishlist-item",
                    data: {
                        'product_id': product_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        alertify.success(response.status || "Moved to cart");
                        $('.wishdata').load(location.href + " .wishdata");
                    }
                });
            }
        });
    });

    //move to wishlist from cart
    $(document).on('click', '.move-to-wishlist', function (e) {
        e.preventDefault();
        var product_id = $(this).closest('.product_data').find('.prod_id').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/add-to-wishlist",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function () {
                $.ajax({
                    method: "POST",
                    url: "/delete-cart-item",
                    data: {
                        'product_id': product_id,
                        csrfmiddlewaretoken: token
                    },
                    success: function (response) {
                        alertify.success(response.status || "Moved to wishlist");
                        $('.cartdata').load(location.href + " .cartdata");
                    }
                });
            }
        });
    });

    //theme toggle
    $(document).on('click', '#themeToggle', function () {
        $('body').toggleClass('dark-theme');
        var isDark = $('body').hasClass('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    //apply saved theme
    if (localStorage.getItem('theme') === 'dark') {
        $('body').addClass('dark-theme');
    }

    //client-side sort/filter on category page
    $(document).on('change', '.sort-select', function () {
        var $cards = $('.book-card-item').parent().get();
        var mode = $(this).val();
        $cards.sort(function (a, b) {
            var $a = $(a).find('.book-card-item');
            var $b = $(b).find('.book-card-item');
            var nameA = $a.data('name');
            var nameB = $b.data('name');
            var priceA = parseFloat($a.data('price'));
            var priceB = parseFloat($b.data('price'));
            if (mode === 'name-asc') return nameA.localeCompare(nameB);
            if (mode === 'name-desc') return nameB.localeCompare(nameA);
            if (mode === 'price-asc') return priceA - priceB;
            if (mode === 'price-desc') return priceB - priceA;
            return 0;
        });
        $.each($cards, function (idx, itm) {
            $('.book-card-item').parent().parent().append(itm);
        });
    });

    $(document).on('keyup', '.filter-input', function () {
        var term = $(this).val().toLowerCase();
        $('.book-card-item').each(function () {
            var author = $(this).data('author');
            if (!term || author.indexOf(term) !== -1) {
                $(this).parent().show();
            } else {
                $(this).parent().hide();
            }
        });
    });

    //checkout toggles
    $(document).on('change', '#sameAsBilling', function () {
        if ($(this).is(':checked')) {
            $('#shippingFields').hide();
        } else {
            $('#shippingFields').show();
        }
    });

    $(document).on('change', 'input[name=payment_choice]', function () {
        var val = $(this).val();
        $('input[name=payment_mode]').val(val);
    });
});
