import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import connection
from core.models import Client
from repositories.RepositoryManager import RepositoryManager
from .forms import ClientForm
import plotly.express as px
import time
import plotly.graph_objects as go
from django.db import connection
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor

def client_list(request):
    clients = Client.objects.all()
    return render(request, 'web/client_list.html', {'clients': clients})

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'web/client_detail.html', {'client': client})

def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'web/client_form.html', {'form': form})

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'web/client_form.html', {'form': form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'web/client_confirm_delete.html', {'client': client})

repo = RepositoryManager()


def dashboard(request):

    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    filter_type = request.GET.get('filter_type')

    equipment_id_filter = request.GET.get('equipment_id')
    instructor_limit_filter = request.GET.get('instructor_limit', 5)
    halls_limit_filter = request.GET.get('hall_limit', 5)

    all_equipment = list(repo.equipment.get_all())
    all_dance_styles = list(repo.dance_styles.get_all())
    all_subscriptions = list(repo.subscriptions.get_all())

    #Clients per Subscription
    subscription_id_filter = request.GET.get('subscription_id')
    dance_style_id_filter = request.GET.get('dance_style_id')
    subs_data = repo.subscriptions.get_subscriptions_with_client_count(subscription_id=subscription_id_filter)
    subs_df = pd.DataFrame(list(subs_data))
    if subs_df.empty:
        subs_df = pd.DataFrame({'name': ['N/A'], 'client_count': [0]})
    subs_fig = px.bar(subs_df, x='name', y='client_count', title='Clients per Subscription')
    subs_graph = subs_fig.to_html(full_html=False)

    #Equipment per Hall
    hall_eq_data = repo.hall_equipment.get_total_equipment_by_hall(equipment_id=equipment_id_filter)
    hall_eq_df = pd.DataFrame(list(hall_eq_data))
    if hall_eq_df.empty:
        hall_eq_df = pd.DataFrame({'hall__name': ['N/A'], 'total_quantity': [0]})
    hall_eq_fig = px.pie(hall_eq_df, names='hall__name', values='total_quantity', title='Equipment per Hall')
    hall_eq_graph = hall_eq_fig.to_html(full_html=False)

    #Revenue by Payment Method
    revenue_df = pd.DataFrame(list(repo.payments.get_revenue_by_method()))
    revenue_fig = px.pie(revenue_df, names='method', values='total_revenue', title='Revenue by Payment Method')
    revenue_graph = revenue_fig.to_html(full_html=False)

    #Top 5 Instructors
    top_inst_df = pd.DataFrame(list(repo.instructors.get_top_instructors(limit=instructor_limit_filter)))
    top_inst_fig = px.bar(top_inst_df, x='name', y='class_count', color='surname', title='Top 5 Instructors')
    top_inst_graph = top_inst_fig.to_html(full_html=False)

    #Monthly Revenue
    min_date_str = request.GET.get('min_date')
    max_date_str = request.GET.get('max_date')
    monthly_df = pd.DataFrame(list(repo.payments.get_monthly_revenue(min_date=min_date_str, max_date=max_date_str)))
    if not monthly_df.empty:
        if 'month_year' in monthly_df.columns:
            monthly_df['month_year'] = pd.to_datetime(monthly_df['month_year'])
            monthly_df['month_year'] = monthly_df['month_year'].dt.strftime('%Y-%m')
        else:
            monthly_df = pd.DataFrame({'month_year': [], 'total_revenue': []})
    else:
        monthly_df = pd.DataFrame({'month_year': [], 'total_revenue': []})

    monthly_fig = px.line(monthly_df, x='month_year', y='total_revenue', title='Monthly Revenue (Filtered)')
    monthly_graph = monthly_fig.to_html(full_html=False)

    #Average Attendees per Class
    hall_eff_data = repo.halls.get_hall_efficiency(limit=halls_limit_filter, dance_style_id=dance_style_id_filter)
    hall_eff_df = pd.DataFrame(list(hall_eff_data))
    if hall_eff_df.empty:
        hall_eff_df = pd.DataFrame({'name': ['N/A'], 'avg_attendees_per_class': [0]})
    hall_eff_fig = px.bar(hall_eff_df, x='name', y='avg_attendees_per_class', title='Average Attendees per Class')
    hall_eff_graph = hall_eff_fig.to_html(full_html=False)

    if is_ajax:
        if filter_type == 'subs':
            return JsonResponse({'subs_graph': subs_graph})
        elif filter_type == 'instructors':
            return JsonResponse({'top_inst_graph': top_inst_graph})
        elif filter_type == 'monthly_revenue':
            return JsonResponse({'monthly_graph': monthly_graph})
        elif filter_type == 'equipment':
            return JsonResponse({'hall_eq_graph': hall_eq_graph})
        elif filter_type == 'revenue':
            return JsonResponse({'revenue_graph': revenue_graph})
        elif filter_type == 'dance_style_efficiency' or filter_type == 'hall_efficiency_limit':
            return JsonResponse({'hall_eff_graph': hall_eff_graph})

        return JsonResponse({})

    context = {
        'subs_graph': subs_graph,
        'all_subscriptions': all_subscriptions,

        'hall_eff_graph': hall_eff_graph,
        'all_dance_styles': all_dance_styles,

        'hall_eq_graph': hall_eq_graph,
        'all_equipment' : all_equipment,

        'revenue_graph' : revenue_graph,

        'top_inst_graph': top_inst_graph,

        'monthly_graph': monthly_graph,
    }
    return render(request, 'web/dashboard.html', context)



def run_single_query():
    start = time.perf_counter()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM client WHERE client_id < 1000 ORDER BY name LIMIT 10;")
        cursor.fetchone()

    duration = time.perf_counter() - start
    return duration


def run_parallel_tests(workers_list=None, total_queries=200):
    results = []
    Executor = ThreadPoolExecutor

    if workers_list is None:
        workers_list = [2 ** k for k in range(0, 10) if 2 ** k <= 256]

    for workers in workers_list:
        max_workers = min(workers, total_queries)

        start_total = time.perf_counter()

        with Executor(max_workers=max_workers) as executor:
            futures = [executor.submit(run_single_query) for _ in range(total_queries)]
            durations = [f.result() for f in futures]

        total_time = time.perf_counter() - start_total
        avg_query_time = sum(durations) / len(durations) if durations else 0

        results.append({
            "workers": workers,
            "total_time": total_time,
            "avg_query_time": avg_query_time,
        })

    df = pd.DataFrame(results)
    return df

def parallel_dashboard(request):
    workers_raw = request.GET.get("workers")

    if workers_raw:
        parts = workers_raw.split(",")
        workers = [int(p) for p in parts]
    else:
        workers = [2 ** k for k in range(0, 10) if 2 ** k <= 256]

    df = run_parallel_tests(workers_list=workers, total_queries=200)

    fig_total = go.Figure()
    fig_total.add_trace(go.Scatter(
        x=df['workers'],
        y=df['total_time'],
        mode='lines+markers',
        name='Total Time (sec)'
    ))
    fig_total.update_layout(
        title=f"Execution time",
        xaxis_title="Threads",
        yaxis_title="Time (sec)",
        hovermode="x unified"
    )
    graph_total = fig_total.to_html(full_html=False, include_plotlyjs='cdn')

    fig_avg = go.Figure()
    fig_avg.add_trace(go.Scatter(
        x=df['workers'],
        y=df['avg_query_time'],
        mode='lines+markers',
        name='Avg Query Time',
        marker=dict(color='red')
    ))
    fig_avg.update_layout(
        title=f"Average request duration",
        xaxis_title="Threads",
        yaxis_title="Average request duration (sec)",
        hovermode="x unified"
    )
    graph_avg = fig_avg.to_html(full_html=False, include_plotlyjs=False)

    return render(
        request,
        "web/parallel_dashboard.html",
        {
            "graph_total": graph_total,
            "graph_avg": graph_avg,
            "df": df.to_html(classes="table table-striped"),
            "current_workers": workers_raw if workers_raw else ",".join(map(str, workers)),
        }
    )
