from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.db import transaction
from django.db.utils import IntegrityError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import razorpay
import json
from .models import Pizza, OrderItem, Order, Customer, PizzaVeggie, PizzaSauce, PizzaBase, PizzaCheese

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def dashboard(request):
    if request.method == "POST":
        pizza_name = json.loads(request.body).get("pizza_name")
        pizza_base = json.loads(request.body).get("pizza_base")
        pizza_cheese = json.loads(request.body).get("pizza_cheese")
        pizza_veggies = json.loads(request.body).get("pizza_veggies")
        pizza_sauces = json.loads(request.body).get("pizza_sauces")
        price = 300

        if pizza_name != "":
            try:
                new_pizza = Pizza.objects.create(name = pizza_name, price = price, 
                                                pizza_base=PizzaBase.objects.get(id=pizza_base), 
                                                pizza_cheese=PizzaCheese.objects.get(id=pizza_cheese), 
                                                custom = True)
                if pizza_veggies:
                    new_pizza.pizza_veggie.set(PizzaVeggie.objects.filter(id__in = pizza_veggies))
                if pizza_sauces:
                    new_pizza.pizza_sauce.set(PizzaSauce.objects.filter(id__in = pizza_sauces))
                new_pizza.save()
                return JsonResponse({"message":"You can now order your custom pizza", "order":1, "pizza_id": str(new_pizza.id)})
            except:
                return JsonResponse({"message":"Please select another pizza name.", "order":0})

    pizza_list = Pizza.objects.filter(custom = False)
    bases = PizzaBase.objects.filter(quantity__gt =0)
    cheeses = PizzaCheese.objects.filter(quantity__gt = 0)
    veggies = PizzaVeggie.objects.filter(quantity__gt = 0)
    sauces = PizzaSauce.objects.filter(is_available = True)
    return render(request, 'dashboard.html', context={"pizzas":pizza_list, 
                                                      "bases":bases, 
                                                      "cheeses":cheeses, 
                                                      "veggies": veggies, 
                                                      "sauces":sauces})

@login_required(login_url="login")
def pizzaBuy(request):
    if request.method == "POST":
        curr_user = request.user
        pizza_id = request.POST.get("pizza_id")

        customer_obj, exist = Customer.objects.get_or_create(user = curr_user)
        customer_obj.save()

        pizza_obj = Pizza.objects.get(id = pizza_id)
        veggies = PizzaVeggie.objects.prefetch_related("pizza_v").filter(pizza_v = pizza_id)
        sauces = PizzaSauce.objects.prefetch_related("pizza_s").filter(pizza_s = pizza_id)

        return render(request, "buyPage.html", {"customer": customer_obj, "pizza":pizza_obj, "pizza_veggies":veggies, "pizza_sauces":sauces})
    return redirect("dashboard")


def paymentInitiator(request):
    if request.method == "POST":
        currency = 'INR'

        curr_user = request.user
        pizza_id = json.loads(request.body).get("pizza_id")
        quantity = json.loads(request.body).get("quantity")

        pizza_obj = Pizza.objects.get(id = int(pizza_id))
        amount = int(pizza_obj.price) * 100 * int(quantity)

        customer_obj, exist = Customer.objects.get_or_create(user = curr_user)
        customer_obj.save()


        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
        
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        with transaction.atomic():
            order_obj = Order.objects.create(customer = customer_obj, payment_status = "pending",order_status="C", razorpay_order_id=razorpay_order_id, amount=(amount/100))
            order_obj.save()

            order_item_obj = OrderItem.objects.create(pizza = pizza_obj, order = order_obj, quantity = quantity)
            order_item_obj.save()

        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        return JsonResponse(context)

@csrf_exempt
def paymentHandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            order_obj = Order.objects.get(razorpay_order_id = razorpay_order_id)

            result = razorpay_client.utility.verify_payment_signature(params_dict)
            
            if result is not None:
                amount = int(order_obj.amount) * 100
                
                try:

                    razorpay_client.payment.capture(payment_id, amount)
                    order_obj.payment_status = "successfull"
                    order_obj.save()
                    try:
                        order_items = order_obj.orderitems.all()
                        for item in order_items:
                            base = item.pizza.pizza_base
                            base.quantity -= item.quantity
                            base.save()

                            cheese = item.pizza.pizza_cheese
                            cheese.quantity -= item.quantity
                            cheese.save()

                            veggies = item.pizza.pizza_veggie.all()
                            for veggie in veggies:
                                veggie.quantity -= item.quantity
                                veggie.save()
                            
                    except BaseException as e:
                        print(e)

                    return render(request, 'message.html', {"heading": "Payment Successfull", "message": "your payment is successfull.", "button":"View Order"})
                except:
                    order_obj.delete()
                    return render(request, 'message.html', {"heading": "Payment Failed", "message": "your payment is unsuccessfull.", "button":"View Order"})
            else:
                order_obj.delete()
                return render(request, 'message.html', {"heading": "Payment Failed", "message": "your payment is unsuccessfull.", "button":"View Order"})

        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()

@login_required(login_url="login")
def profilePage(request):
    if request.method == "GET":
        curr_user = request.user
        curr_customer, exist = Customer.objects.get_or_create(user = curr_user)

        orders = Order.objects.prefetch_related("orderitems").filter(customer = curr_customer).filter(payment_status = "successfull")
        return render(request, "profile.html", {"customer": curr_customer, "orders":orders})
    return HttpResponseBadRequest()

@login_required(login_url="login")    
def updateProfile(request):
    if request.method ==  "POST":
        try:
            first_name = json.loads(request.body).get("first_name")
            last_name = json.loads(request.body).get("last_name")
            add_l1 = json.loads(request.body).get("add_l1")
            add_l2 = json.loads(request.body).get("add_l2")
            pincode = json.loads(request.body).get("pincode")
            city = json.loads(request.body).get("city")
            state = json.loads(request.body).get("state")
            country = json.loads(request.body).get("country")

            curr_user = request.user
            if first_name:
                curr_user.first_name = first_name
                curr_user.last_name = last_name
                curr_user.save()

            curr_customer = Customer.objects.get(user = curr_user)
            curr_customer.address_line1 = add_l1
            curr_customer.address_line2 = add_l2
            curr_customer.pincode = pincode
            curr_customer.city = city
            curr_customer.state = state
            curr_customer.country = country
            curr_customer.save()
            
            return JsonResponse("Profile updated successfully", safe=False)
        except IntegrityError as e:
            print(e)
            return JsonResponse("Profile updation failed. May be due to an empty field.", safe=False)

    return HttpResponseBadRequest()


