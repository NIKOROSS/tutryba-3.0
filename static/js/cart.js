document.addEventListener('DOMContentLoaded', function() {
    // Обработка форм добавления в корзину
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const productId = this.dataset.productId;
            const quantity = this.querySelector('.quantity-input').value;
            const url = `/cart/add/${productId}/`;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `quantity=${quantity}&csrfmiddlewaretoken=${getCookie('csrftoken')}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Обновляем счетчик товаров в корзине
                    const cartCount = document.querySelector('.cart-count');
                    if (cartCount) {
                        cartCount.textContent = data.cart_total;
                    }
                    // Показываем уведомление об успехе
                    showNotification(data.message);
                } else {
                    // Показываем ошибку
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Ошибка при добавлении товара', 'error');
            });
        });
    });

    // Обработка кнопок увеличения/уменьшения количества
    document.querySelectorAll('.increase-quantity, .decrease-quantity').forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.quantity-input');
            const currentValue = parseInt(input.value);
            const maxValue = parseInt(input.dataset.max);
            
            if (this.classList.contains('increase-quantity')) {
                if (currentValue < maxValue) {
                    input.value = currentValue + 1;
                }
            } else {
                if (currentValue > 1) {
                    input.value = currentValue - 1;
                }
            }
        });
    });
});

// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для показа уведомлений
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'success' ? 'success' : 'danger'} notification`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function updateCartTotal(total) {
    const cartTotalElement = document.querySelector('.cart-total');
    if (cartTotalElement) {
        cartTotalElement.textContent = `${total} ₽`;
    }
} 