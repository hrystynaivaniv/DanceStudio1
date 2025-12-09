import pandas as pd
from django.shortcuts import render
from django.views import View
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.transform import cumsum
from bokeh.embed import components
from math import pi
from bokeh.palettes import Category10, Spectral6, Turbo256
from repositories.RepositoryManager import RepositoryManager

class BokehDashboardView(View):
    def get(self, request):
        repo = RepositoryManager()
        plots = {}

        instructor_limit = int(request.GET.get('instructor_limit', 5) or 5)
        halls_limit = int(request.GET.get('hall_limit', 5) or 5)
        min_date = request.GET.get('min_date')
        max_date = request.GET.get('max_date')

        # Clients per Subscription
        df_subs = pd.DataFrame(list(repo.subscriptions.get_subscriptions_with_client_count()))
        if df_subs.empty:
            df_subs = pd.DataFrame({'name': ['N/A'], 'client_count': [0]})
        df_subs['client_count'] = df_subs['client_count'].astype(float)
        source_subs = ColumnDataSource(df_subs)
        p_subs = figure(x_range=df_subs['name'].tolist(), height=400, title="1. Clients per Subscription",
                        toolbar_location=None, tools="", x_axis_label="Subscription Name", y_axis_label="Client Count")
        p_subs.vbar(x='name', top='client_count', width=0.9, source=source_subs,
                    line_color='white', fill_color=Category10[3][0])
        p_subs.add_tools(HoverTool(tooltips=[("Subscription", "@name"), ("Clients", "@client_count")]))
        plots['chart_subs'] = p_subs

        # Equipment per Hall
        df_hall_eq = pd.DataFrame(list(repo.hall_equipment.get_total_equipment_by_hall()))
        if df_hall_eq.empty:
            df_hall_eq = pd.DataFrame({'hall__name': ['N/A'], 'total_quantity': [0]})
        df_hall_eq['total_quantity'] = df_hall_eq['total_quantity'].astype(float)
        total = df_hall_eq['total_quantity'].sum()
        df_hall_eq['angle'] = df_hall_eq['total_quantity'] / total * 2 * pi
        df_hall_eq['color'] = Category10[len(df_hall_eq)] if len(df_hall_eq) <= 10 else Turbo256[:len(df_hall_eq)]
        source_hall_eq = ColumnDataSource(df_hall_eq)
        p_hall_eq = figure(height=400, title="2. Equipment per Hall", toolbar_location=None, tools="hover",
                           tooltips="@hall__name: @total_quantity", x_range=(-0.5, 1))
        p_hall_eq.wedge(x=0, y=1, radius=0.4,
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='hall__name', source=source_hall_eq)
        p_hall_eq.axis.visible = False
        p_hall_eq.grid.grid_line_color = None
        plots['chart_hall_eq'] = p_hall_eq

        # Revenue by Payment Method
        df_revenue = pd.DataFrame(list(repo.payments.get_revenue_by_method()))
        df_revenue['total_revenue'] = df_revenue['total_revenue'].astype(float)
        total_rev = df_revenue['total_revenue'].sum()
        df_revenue['angle'] = df_revenue['total_revenue'] / total_rev * 2 * pi
        df_revenue['color'] = Category10[len(df_revenue)] if len(df_revenue) <= 10 else Spectral6[:len(df_revenue)]
        source_revenue = ColumnDataSource(df_revenue)
        p_revenue = figure(height=400, title="3. Revenue by Payment Method", toolbar_location=None, tools="hover",
                           tooltips="@method: @total_revenue", x_range=(-0.5, 1))
        p_revenue.wedge(x=0, y=1, radius=0.4,
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='method', source=source_revenue)
        p_revenue.axis.visible = False
        p_revenue.grid.grid_line_color = None
        plots['chart_revenue'] = p_revenue

        # Top Instructors
        df_inst = pd.DataFrame(list(repo.instructors.get_top_instructors(limit=instructor_limit)))
        if df_inst.empty:
            df_inst = pd.DataFrame({'name': ['N/A'], 'surname': ['N/A'], 'class_count': [0]})
        df_inst['full_name'] = df_inst['name'] + ' ' + df_inst['surname']
        df_inst = df_inst.sort_values('class_count', ascending=True)
        source_inst = ColumnDataSource(df_inst)
        p_inst = figure(y_range=df_inst['full_name'].tolist(), height=400,
                        title=f"4. Top {instructor_limit} Instructors",
                        toolbar_location=None, tools="", y_axis_label="Instructor", x_axis_label="Class Count")
        p_inst.hbar(y='full_name', right='class_count', height=0.9, source=source_inst,
                    line_color='white', fill_color=Category10[3][1])
        p_inst.add_tools(HoverTool(tooltips=[("Classes", "@class_count")]))
        plots['chart_inst'] = p_inst

        # Monthly Revenue
        df_monthly = pd.DataFrame(list(repo.payments.get_monthly_revenue(min_date=min_date, max_date=max_date)))
        if not df_monthly.empty and 'month_year' in df_monthly.columns:
            df_monthly['month_year_dt'] = pd.to_datetime(df_monthly['month_year'])
            df_monthly = df_monthly.sort_values('month_year_dt')
            df_monthly['month_year_str'] = df_monthly['month_year_dt'].dt.strftime('%Y-%m')
            df_monthly['total_revenue'] = df_monthly['total_revenue'].astype(float)
            source_monthly = ColumnDataSource(df_monthly)
            p_monthly = figure(x_range=df_monthly['month_year_str'].tolist(), height=400,
                               title="5. Monthly Revenue",
                               toolbar_location=None, tools="pan,wheel_zoom,box_zoom,reset,save")
            p_monthly.line(x='month_year_str', y='total_revenue', source=source_monthly, line_width=2,
                           color=Category10[3][2])
            p_monthly.circle(x='month_year_str', y='total_revenue', source=source_monthly, size=8,
                             color=Category10[3][2], legend_label="Revenue")
            p_monthly.xaxis.major_label_orientation = pi / 4
            p_monthly.add_tools(HoverTool(tooltips=[("Date", "@month_year_str"), ("Revenue", "@total_revenue")]))
        else:
            p_monthly = figure(height=400, title="5. Monthly Revenue (No Data)", toolbar_location=None)
        plots['chart_monthly'] = p_monthly

        # Avg Attendees per Class
        df_hall_eff = pd.DataFrame(list(repo.halls.get_hall_efficiency(limit=halls_limit)))
        if df_hall_eff.empty:
            df_hall_eff = pd.DataFrame({'name': ['N/A'], 'avg_attendees_per_class': [0.0]})
        df_hall_eff['avg_attendees_per_class'] = df_hall_eff['avg_attendees_per_class'].astype(float)
        source_hall_eff = ColumnDataSource(df_hall_eff)
        p_hall_eff = figure(x_range=df_hall_eff['name'].tolist(), height=400,
                            title=f"6. Avg Attendees per Class (Top {halls_limit} Halls)",
                            toolbar_location=None, tools="", x_axis_label="Hall Name", y_axis_label="Avg Attendees")
        p_hall_eff.vbar(x='name', top='avg_attendees_per_class', width=0.9, source=source_hall_eff,
                        line_color='white', fill_color=Category10[3][2])
        p_hall_eff.add_tools(HoverTool(tooltips=[("Hall", "@name"), ("Avg Attendees", "@avg_attendees_per_class")]))
        p_hall_eff.xaxis.major_label_orientation = pi / 4
        plots['chart_hall_eff'] = p_hall_eff

        script, divs = components(plots)

        context = {
            'script': script,
            'divs': divs,
            'limit_options': [3, 5, 10, 20],
            'current_instructor_limit': instructor_limit,
            'current_min_date': min_date,
            'current_max_date': max_date,
            'current_hall_limit': halls_limit,
            'all_equipment': list(repo.equipment.get_all()),
            'all_dance_styles': list(repo.dance_styles.get_all()),
            'all_subscriptions': list(repo.subscriptions.get_all()),
        }

        return render(request, 'web/dashboard_bokeh.html', context)
