from .cart import Cart

def cart(request):
    """Контекстный процессор для передачи корзины во все шаблоны"""
    return {'cart': Cart(request)}
