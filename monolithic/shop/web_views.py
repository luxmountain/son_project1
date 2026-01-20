"""
Web Views for Monolithic Architecture - Frontend
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from decimal import Decimal
from .models import Customer, Book, Cart, CartItem


# ==================== Home ====================

def home(request):
    """Home page"""
    context = {
        'book_count': Book.objects.count(),
        'customer_count': Customer.objects.count(),
        'cart_count': Cart.objects.count(),
        'recent_books': Book.objects.order_by('-created_at')[:6],
    }
    return render(request, 'home.html', context)


# ==================== Book Views ====================

def book_list(request):
    """List all books"""
    books = Book.objects.all()
    
    # Search
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    
    # Filter by stock
    stock_filter = request.GET.get('stock')
    if stock_filter == 'in_stock':
        books = books.filter(stock__gt=0)
    elif stock_filter == 'out_of_stock':
        books = books.filter(stock=0)
    
    return render(request, 'books/book_list.html', {'books': books})


def book_detail(request, book_id):
    """Book detail page"""
    book = get_object_or_404(Book, id=book_id)
    customers = Customer.objects.all()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'customers': customers
    })


def book_create(request):
    """Create new book"""
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            price=Decimal(request.POST.get('price', '0')),
            stock=int(request.POST.get('stock', 0))
        )
        messages.success(request, 'Thêm sách thành công!')
        return redirect('book_list')
    
    return render(request, 'books/book_form.html')


def book_edit(request, book_id):
    """Edit book"""
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.price = Decimal(request.POST.get('price', '0'))
        book.stock = int(request.POST.get('stock', 0))
        book.save()
        messages.success(request, 'Cập nhật sách thành công!')
        return redirect('book_detail', book_id=book.id)
    
    return render(request, 'books/book_form.html', {'book': book})


def book_delete(request, book_id):
    """Delete book"""
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Xóa sách thành công!')
    return redirect('book_list')


# ==================== Customer Views ====================

def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'customers/customer_list.html', {'customers': customers})


def customer_detail(request, customer_id):
    """Customer detail page"""
    customer = get_object_or_404(Customer, id=customer_id)
    return render(request, 'customers/customer_detail.html', {'customer': customer})


def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        Customer.objects.create(
            user_name=request.POST.get('user_name'),
            password=request.POST.get('password'),
            phone_number=request.POST.get('phone_number') or None,
            dob=request.POST.get('dob') or None
        )
        messages.success(request, 'Thêm khách hàng thành công!')
        return redirect('customer_list')
    
    return render(request, 'customers/customer_form.html')


def customer_edit(request, customer_id):
    """Edit customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer.user_name = request.POST.get('user_name')
        customer.phone_number = request.POST.get('phone_number') or None
        dob = request.POST.get('dob')
        customer.dob = dob if dob else None
        customer.save()
        messages.success(request, 'Cập nhật khách hàng thành công!')
        return redirect('customer_detail', customer_id=customer.id)
    
    return render(request, 'customers/customer_form.html', {'customer': customer})


def customer_delete(request, customer_id):
    """Delete customer"""
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    messages.success(request, 'Xóa khách hàng thành công!')
    return redirect('customer_list')


def customer_cart(request, customer_id):
    """View customer's cart"""
    customer = get_object_or_404(Customer, id=customer_id)
    cart, created = Cart.objects.get_or_create(customer=customer)
    return render(request, 'carts/cart_detail.html', {'cart': cart})


# ==================== Cart Views ====================

def cart_list(request):
    """List all carts"""
    carts = Cart.objects.all().order_by('-created_at')
    return render(request, 'carts/cart_list.html', {'carts': carts})


def cart_detail(request, cart_id):
    """Cart detail page"""
    cart = get_object_or_404(Cart, id=cart_id)
    return render(request, 'carts/cart_detail.html', {'cart': cart})


def add_to_cart(request):
    """Add item to cart"""
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        book_id = request.POST.get('book_id')
        quantity = int(request.POST.get('quantity', 1))
        
        customer = get_object_or_404(Customer, id=customer_id)
        book = get_object_or_404(Book, id=book_id)
        
        if book.stock < quantity:
            messages.error(request, 'Không đủ hàng trong kho!')
            return redirect('book_detail', book_id=book_id)
        
        cart, created = Cart.objects.get_or_create(customer=customer)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        messages.success(request, f'Đã thêm "{book.title}" vào giỏ hàng!')
        return redirect('cart_detail', cart_id=cart.id)
    
    return redirect('book_list')


def cart_remove_item(request, cart_id, book_id):
    """Remove item from cart"""
    cart = get_object_or_404(Cart, id=cart_id)
    CartItem.objects.filter(cart=cart, book_id=book_id).delete()
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng!')
    return redirect('cart_detail', cart_id=cart_id)


def cart_update_quantity(request, item_id):
    """Update cart item quantity"""
    if request.method == 'POST':
        item = get_object_or_404(CartItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > item.book.stock:
            messages.error(request, 'Không đủ hàng trong kho!')
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, 'Đã cập nhật số lượng!')
        
        return redirect('cart_detail', cart_id=item.cart.id)
    
    return redirect('cart_list')


def cart_clear(request, cart_id):
    """Clear all items from cart"""
    cart = get_object_or_404(Cart, id=cart_id)
    cart.items.all().delete()
    messages.success(request, 'Đã xóa tất cả sản phẩm trong giỏ hàng!')
    return redirect('cart_detail', cart_id=cart_id)


def cart_checkout(request, cart_id):
    """Checkout cart"""
    if request.method == 'POST':
        cart = get_object_or_404(Cart, id=cart_id)
        
        if not cart.items.exists():
            messages.error(request, 'Giỏ hàng trống!')
            return redirect('cart_detail', cart_id=cart_id)
        
        # Check stock
        for item in cart.items.all():
            if item.book.stock < item.quantity:
                messages.error(request, f'Không đủ hàng cho "{item.book.title}"!')
                return redirect('cart_detail', cart_id=cart_id)
        
        # Process checkout
        total = cart.total_price
        for item in cart.items.all():
            item.book.reduce_stock(item.quantity)
        
        # Clear cart
        cart.items.all().delete()
        
        messages.success(request, f'Thanh toán thành công! Tổng tiền: ${total}')
        return redirect('home')
    
    return redirect('cart_detail', cart_id=cart_id)
