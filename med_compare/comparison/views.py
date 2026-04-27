from django.shortcuts import render, redirect
from .utils import get_medicine_prices
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import SearchHistory


# 🔹 Problem → Medicine Mapping
PROBLEM_MEDICINE_MAP = {
    "fever": ["dolo 650", "paracetamol"],
    "headache": ["saridon", "paracetamol"],
    "cold": ["cetirizine", "sinarest"],
    "cough": ["benadryl", "ascaril"],
    "allergy": ["cetirizine", "loratadine"],
    "stomach pain": ["meftal spas", "cyclopam"],
    "acidity": ["gelusil", "pantoprazole"],
    "vomiting": ["ondem", "domstal"],
    "eye irritation": ["refresh tears", "itone eye drops"],
    "body pain": ["brufen", "combiflam"],
}


# 🏠 HOME
def home(request):
    return render(request, 'comparison/index.html')


# 🔎 SEARCH BY MEDICINE
def search_medicine(request):
    if request.method == "POST":
        medicine_name = request.POST.get('medicine_name', '').strip().replace(']', '')

        # ✅ SAVE HISTORY
        if request.user.is_authenticated and medicine_name:
            SearchHistory.objects.create(
                user=request.user,
                search_type='medicine',
                query=medicine_name
            )

        results = get_medicine_prices(medicine_name)

        cleaned_prices = []

        for res in results:
            try:
                price = float(str(res['price']).replace('₹', '').strip())
                res['price'] = price
                cleaned_prices.append(price)
            except:
                res['price'] = None

        cheapest_price = min(cleaned_prices) if cleaned_prices else None
        max_price = max(cleaned_prices) if cleaned_prices else None

        for res in results:
            if res['price'] and max_price:
                savings = ((max_price - res['price']) / max_price) * 100
                res['savings_percent'] = round(savings)
            else:
                res['savings_percent'] = 0

        context = {
            'medicine': medicine_name.upper(),
            'results': results,
            'cheapest_price': cheapest_price,
        }

        return render(request, 'comparison/results.html', context)

    return redirect('home')


# 🤖 SEARCH BY PROBLEM
def search_by_problem(request):
    if request.method == "POST":
        problem = request.POST.get('problem', '').strip().lower()

        # ✅ SAVE HISTORY
        if request.user.is_authenticated and problem:
            SearchHistory.objects.create(
                user=request.user,
                search_type='problem',
                query=problem
            )

        suggested_medicines = PROBLEM_MEDICINE_MAP.get(problem)

        if not suggested_medicines:
            return render(request, 'comparison/problem_results.html', {
                'problem': problem.upper(),
                'error': "No suggestions found for this problem."
            })

        all_results = []

        for med in suggested_medicines:
            results = get_medicine_prices(med)

            cleaned_prices = []

            for res in results:
                try:
                    price = float(str(res['price']).replace('₹', '').strip())
                    res['price'] = price
                    cleaned_prices.append(price)
                except:
                    res['price'] = None

            cheapest_price = min(cleaned_prices) if cleaned_prices else None
            max_price = max(cleaned_prices) if cleaned_prices else None

            for res in results:
                if res['price'] and max_price:
                    savings = ((max_price - res['price']) / max_price) * 100
                    res['savings_percent'] = round(savings)
                else:
                    res['savings_percent'] = 0

            all_results.append({
                'medicine': med.upper(),
                'results': results,
                'cheapest_price': cheapest_price
            })

        return render(request, 'comparison/problem_results.html', {
            'problem': problem.upper(),
            'medicines_data': all_results
        })

    return redirect('home')


# 🔐 REGISTER
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'comparison/register.html')


# 📜 HISTORY PAGE
@login_required
def history(request):
    history_data = SearchHistory.objects.filter(user=request.user).order_by('-searched_at')

    return render(request, 'comparison/history.html', {
        'history': history_data
    })
    
#for deleting history
@login_required
def delete_history(request, id):
    if request.method == "POST":
        try:
            record = SearchHistory.objects.get(id=id, user=request.user)
            record.delete()
        except SearchHistory.DoesNotExist:
            pass

    return redirect('history')