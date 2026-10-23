import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(page_title="Виртуальная лаборатория материаловедения", page_icon="💎", layout="wide")
st.title("💎 Виртуальная лаборатория материаловедения")
st.markdown("Добро пожаловать в интерактивную среду для изучения свойств металлов и сплавов!")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🔷 Кристаллические решётки", "📈 Диаграмма Fe-C", "🔩 Измерение твёрдости", "🤖 AI-помощник"])

# ==========================================
# ВКЛАДКА 1: 3D МОДЕЛЬ
# ==========================================
with tab1:
    st.markdown("### Интерактивная 3D-модель кристаллических решёток")
    
    st.info("""
    💡 **Зачем это нужно?**  
    Кристаллическая решётка — это «ДНК» металла. Именно то, как упакованы атомы (ОЦК, ГЦК или ГПУ), определяет, будет ли металл гнуться, как медь, или оставаться твёрдым.  
    В этой вкладке учащийся может вращать модель, менять температуру и наглядно увидеть, как перестраивается структура. Это объясняет, почему сталь можно ковать только в нагретом состоянии, а при комнатной температуре её можно только точить.
    """)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        material = st.selectbox("Материал:", ["Сталь 20", "Сталь 45", "Алюминий", "Медь", "Титан"])
    with col2:
        temp = st.slider("Температура, °C", 20, 1600, 20, 50)

    if material in ["Сталь 20", "Сталь 45"]:
        if temp < 911:
            lat, phase = "ОЦК", "Феррит (ОЦК)"
            st.warning(f"📊 **Фаза:** {phase}")
        elif temp < 1392:
            lat, phase = "ГЦК", "Аустенит (ГЦК)"
            st.success(f"📊 **Фаза:** {phase}")
        else:
            lat, phase = "ОЦК", "δ-железо (ОЦК)"
            st.info(f"📊 **Фаза:** {phase}")
    elif material == "Титан":
        if temp < 882:
            lat, phase = "ГПУ", "α-титан (ГПУ)"
            st.warning(f"📊 **Фаза:** {phase}")
        else:
            lat, phase = "ОЦК", "β-титан (ОЦК)"
            st.success(f"📊 **Фаза:** {phase}")
    else:
        lat, phase = "ГЦК", "ГЦК (стабильная)"
        st.info(f"📊 **Фаза:** {phase}")

    fig = go.Figure()
    if lat == "ОЦК":
        v = np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]])
        edges = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
        for e in edges:
            fig.add_trace(go.Scatter3d(x=[v[e[0],0],v[e[1],0]], y=[v[e[0],1],v[e[1],1]], z=[v[e[0],2],v[e[1],2]], mode='lines', line=dict(color='gray', width=2), showlegend=False))
        for v_i in v:
            fig.add_trace(go.Scatter3d(x=[0.5,v_i[0]], y=[0.5,v_i[1]], z=[0.5,v_i[2]], mode='lines', line=dict(color='red', width=1.5, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=v[:,0], y=v[:,1], z=v[:,2], mode='markers', marker=dict(size=14, color='blue'), name='Вершины'))
        fig.add_trace(go.Scatter3d(x=[0.5], y=[0.5], z=[0.5], mode='markers', marker=dict(size=18, color='red'), name='Центр'))
    elif lat == "ГЦК":
        v = np.array([[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]])
        edges = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]]
        for e in edges:
            fig.add_trace(go.Scatter3d(x=[v[e[0],0],v[e[1],0]], y=[v[e[0],1],v[e[1],1]], z=[v[e[0],2],v[e[1],2]], mode='lines', line=dict(color='gray', width=2), showlegend=False))
        f = np.array([[0.5,0.5,0],[0.5,0.5,1],[0.5,0,0.5],[0.5,1,0.5],[0,0.5,0.5],[1,0.5,0.5]])
        fc = [[0,[0,1,2,3]], [1,[4,5,6,7]], [2,[0,1,5,4]], [3,[2,3,7,6]], [4,[0,3,7,4]], [5,[1,2,6,5]]]
        for fi, vi in fc:
            for vi_i in vi:
                fig.add_trace(go.Scatter3d(x=[f[fi,0],v[vi_i,0]], y=[f[fi,1],v[vi_i,1]], z=[f[fi,2],v[vi_i,2]], mode='lines', line=dict(color='green', width=1.5, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=v[:,0], y=v[:,1], z=v[:,2], mode='markers', marker=dict(size=14, color='blue'), name='Вершины'))
        fig.add_trace(go.Scatter3d(x=f[:,0], y=f[:,1], z=f[:,2], mode='markers', marker=dict(size=16, color='green'), name='Грани'))
    else:
        b = np.array([[0,0,0],[1,0,0],[1.5,0.866,0],[1,1.732,0],[0,1.732,0],[-0.5,0.866,0]])
        t = b + np.array([0,0,1.633])
        m = np.array([[0.5,0.289,0.816],[1,1.155,0.816],[0.5,1.444,0.816]])
        for i in range(6):
            fig.add_trace(go.Scatter3d(x=[b[i,0],b[(i+1)%6,0]], y=[b[i,1],b[(i+1)%6,1]], z=[b[i,2],b[(i+1)%6,2]], mode='lines', line=dict(color='gray', width=2), showlegend=False))
            fig.add_trace(go.Scatter3d(x=[t[i,0],t[(i+1)%6,0]], y=[t[i,1],t[(i+1)%6,1]], z=[t[i,2],t[(i+1)%6,2]], mode='lines', line=dict(color='gray', width=2), showlegend=False))
            fig.add_trace(go.Scatter3d(x=[b[i,0],t[i,0]], y=[b[i,1],t[i,1]], z=[b[i,2],t[i,2]], mode='lines', line=dict(color='gray', width=2), showlegend=False))
        for m_i in m:
            fig.add_trace(go.Scatter3d(x=[m_i[0],m_i[0]], y=[m_i[1],m_i[1]], z=[0,m_i[2]], mode='lines', line=dict(color='orange', width=1.5, dash='dot'), showlegend=False))
            fig.add_trace(go.Scatter3d(x=[m_i[0],m_i[0]], y=[m_i[1],m_i[1]], z=[m_i[2],1.633], mode='lines', line=dict(color='orange', width=1.5, dash='dot'), showlegend=False))
        fig.add_trace(go.Scatter3d(x=b[:,0], y=b[:,1], z=b[:,2], mode='markers', marker=dict(size=14, color='blue'), name='Низ'))
        fig.add_trace(go.Scatter3d(x=t[:,0], y=t[:,1], z=t[:,2], mode='markers', marker=dict(size=14, color='blue'), name='Верх'))
        fig.add_trace(go.Scatter3d(x=m[:,0], y=m[:,1], z=m[:,2], mode='markers', marker=dict(size=16, color='orange'), name='Средний'))

    fig.update_layout(scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False)), height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 📝 Задания для учащегося")
    if lat == "ОЦК":
        st.info("💡 **Задание 1:** Посчитайте атомы. **Подсказка:** 8×1/8 + 1 = 2 атома")
        st.info("💡 **Задание 2:** Почему ОЦК менее пластична? **Подсказка:** Атом в центре мешает скольжению.")
    elif lat == "ГЦК":
        st.success("💡 **Задание 1:** Атомы в гранях. **Подсказка:** 6×1/2 = 3 атома. Всего 4.")
        st.success("💡 **Задание 2:** Почему сталь куют при 1200°C? **Подсказка:** ГЦК максимально пластична.")
    else:
        st.warning("💡 **Задание 1:** Сколько слоёв в ГПУ? **Подсказка:** 3 слоя.")
        st.warning("💡 **Задание 2:** Почему титан трудно обрабатывать? **Подсказка:** ГПУ мало плоскостей скольжения.")

    st.markdown("---")
    st.markdown(f"### 🔧 Применение при {temp}°C")
    if material in ["Сталь 20", "Сталь 45"]:
        if temp < 911: st.markdown("✅ Механическая обработка | ❌ Нельзя ковать")
        else: st.markdown("✅ Горячая ковка и штамповка (оптимально 1100-1200°C)")
    elif material == "Алюминий": st.markdown("✅ Отличная пластичность | ✅ Штамповка")
    elif material == "Медь": st.markdown("✅ Волочение проволоки | ✅ Штамповка")
    elif material == "Титан":
        if temp < 882: st.markdown("⚠️ Ограниченная пластичность (ГПУ)")
        else: st.markdown("✅ Горячая ковка (ОЦК)")

# ==========================================
# ВКЛАДКА 2: ДИАГРАММА Fe-C
# ==========================================
with tab2:
    st.markdown("### 🔥 Диаграмма состояния железо-углерод (Fe-C)")
    
    st.info("""
    💡 **Зачем это нужно?**  
    Диаграмма «Железо-Углерод» — это главная карта металлурга. Она показывает, в каком состоянии находится сталь или чугун при нагреве.  
    Двигая ползунок температуры, учащийся видит «путь нагрева» (зелёная линия): как твёрдый феррит превращается в пластичный аустенит. Это наглядно объясняет, *почему* сталь куют только в раскалённом виде, а чугун можно только лить.
    """)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        mat_fe = st.selectbox("Материал:", ["Сталь 20 (0,20% C)", "Сталь 45 (0,45% C)", "Сталь 0,8% C", "Чугун 3% C", "Железо (0% C)"])
    with col2:
        temp_fe = st.slider("🌡️ Температура, °C", 20, 1600, 20, 10)
    
    c_map = {"Сталь 20 (0,20% C)": 0.20, "Сталь 45 (0,45% C)": 0.45, "Сталь 0,8% C": 0.8, "Чугун 3% C": 3.0, "Железо (0% C)": 0.0}
    C = c_map[mat_fe]

    fig_fe = go.Figure()
    fig_fe.add_trace(go.Scatter(x=[0, 6.67, 6.67, 0], y=[1538, 1147, 1600, 1600], fill='toself', fillcolor='#FFFACD', line=dict(color='orange', width=1), name='Жидкость (L)'))
    fig_fe.add_annotation(x=3.5, y=1400, text="ЖИДКОСТЬ", showarrow=False, font=dict(size=14, color='orange', family='Arial Black'))
    fig_fe.add_trace(go.Scatter(x=[0.0218, 0.8, 2.14, 2.14, 0.8, 0.0218], y=[727, 727, 727, 1147, 1495, 911], fill='toself', fillcolor='#FFB6C1', line=dict(color='red', width=2), name='Аустенит (γ)'))
    fig_fe.add_annotation(x=1.2, y=1000, text="АУСТЕНИТ (γ)<br>ГЦК", showarrow=False, font=dict(size=14, color='red', family='Arial Black'))
    fig_fe.add_trace(go.Scatter(x=[0, 0.0218, 0.0218, 0], y=[0, 0, 727, 911], fill='toself', fillcolor='#ADD8E6', line=dict(color='blue', width=2), name='Феррит (α)'))
    fig_fe.add_annotation(x=0.01, y=500, text="ФЕРРИТ (α)<br>ОЦК", showarrow=False, font=dict(size=12, color='blue', family='Arial Black'))
    fig_fe.add_trace(go.Scatter(x=[6.67, 6.67, 2.14, 2.14], y=[0, 1600, 1147, 727], fill='toself', fillcolor='#D3D3D3', line=dict(color='gray', width=2), name='Цементит'))
    fig_fe.add_annotation(x=4.5, y=900, text="ЦЕМЕНТИТ", showarrow=False, font=dict(size=12, color='gray', family='Arial Black'))
    fig_fe.add_trace(go.Scatter(x=[0.0218, 6.67, 6.67, 0.0218], y=[0, 0, 727, 727], fill='toself', fillcolor='#E6E6FA', line=dict(color='purple', width=1, dash='dot'), name='Перлит'))
    fig_fe.add_annotation(x=3, y=400, text="ПЕРЛИТ", showarrow=False, font=dict(size=12, color='purple', family='Arial Black'))
    fig_fe.add_trace(go.Scatter(x=[0, 6.67], y=[727, 727], mode='lines', line=dict(color='black', width=2, dash='dash'), name='Линия A1 (727°C)'))
    fig_fe.add_annotation(x=5, y=727, text="A1 (727°C)", showarrow=False, font=dict(size=11, color='black'))
    fig_fe.add_trace(go.Scatter(x=[C, C], y=[20, temp_fe], mode='lines', line=dict(color='#00FF00', width=5), name='Путь нагрева'))
    fig_fe.add_trace(go.Scatter(x=[C], y=[temp_fe], mode='markers+text', marker=dict(color='#FFFF00', size=22, symbol='star', line=dict(color='red', width=2)), text=[f' {temp_fe}°C'], textposition='middle right', textfont=dict(size=14, color='black', family='Arial Black'), showlegend=False))
    fig_fe.update_layout(xaxis_title="% C", yaxis_title="Температура, °C", xaxis=dict(range=[-0.2, 7]), yaxis=dict(range=[0, 1650]), height=600, plot_bgcolor='white')
    st.plotly_chart(fig_fe, use_container_width=True)

    st.markdown("---")
    st.markdown("### 🔍 Что происходит сейчас?")
    if temp_fe < 727:
        st.error(f"🔵 **{temp_fe}°C:** Феррит/Перлит (ОЦК). Материал твёрдый. **Ковка невозможна!**")
    elif 727 <= temp_fe < 911 and C < 0.8:
        st.warning(f"🟣 **{temp_fe}°C:** Переходная зона. ⚠️ Фазовое превращение ОЦК → ГЦК.")
    elif 911 <= temp_fe < 1147 and C < 2.14:
        st.success(f"🔴 **{temp_fe}°C:** АУСТЕНИТ (ГЦК)! ✅ **МАКСИМАЛЬНАЯ ПЛАСТИЧНОСТЬ!** Сталь можно ковать!")
    elif temp_fe >= 1147 and C > 2.14:
        st.info(f"🟡 **{temp_fe}°C:** Чугун плавится. Только литьё.")
    else:
        st.info(f"⚪ **{temp_fe}°C:** Высокие температуры. Близко к плавлению.")

    st.markdown("---")
    st.markdown("### 📝 Вопросы с ответами")
    with st.expander("❓ Почему сталь куют при 1100-1200°C?"):
        st.markdown("При нагреве выше 911°C твёрдая ОЦК-решётка (феррит) перестраивается в пластичную ГЦК-решётку (аустенит). Слои атомов начинают легко скользить, как колода карт.")
    with st.expander("❓ Почему чугун (3% C) нельзя ковать?"):
        st.markdown("У чугуна нет зоны чистого аустенита. В структуре всегда присутствует хрупкий цементит (Fe3C), который не дает металлу деформироваться. Чугун только льют!")
    with st.expander("❓ Что происходит при 727°C (линия A1)?"):
        st.markdown("Эвтектоидное превращение: Аустенит (γ) → Перлит (Феррит + Цементит). Сталь теряет пластичность и становится твёрдой.")
    with st.expander("❓ Температура ковки для стали 45?"):
        st.markdown("Сталь 45 (0,45% C) куют в диапазоне **1100-1200°C**. Это красная зона аустенита на диаграмме.")

# ==========================================
# ВКЛАДКА 3: ИЗМЕРЕНИЕ ТВЁРДОСТИ
# ==========================================
with tab3:
    st.markdown("### 🔩 Интерактивный калькулятор твёрдости")
    
    st.info("""
    💡 **Зачем это нужно?**  
    Твёрдость — главный показатель качества детали. Но один метод не подходит для всего: мягкий алюминий нельзя мерить алмазом, а закалённую сталь не продавить шариком.  
    В этой вкладке учащийся выступает в роли лаборанта: выбирает метод, вводит параметры реального испытания, видит схему отпечатка и мгновенно получает результат, понимая практическую разницу между методами Бринелля, Роквелла и Виккерса.
    """)
    st.markdown("---")
    
    method = st.selectbox("📏 Метод измерения твёрдости:", ["По Бринеллю (HB)", "По Роквеллу (HRC/HRB)", "По Виккерсу (HV)"])
    st.markdown("---")
    
    if method == "По Бринеллю (HB)":
        st.markdown("#### 🔵 Метод Бринелля")
        st.markdown("**Суть:** Вдавливание стального шарика диаметром D под нагрузкой P. Измеряется диаметр отпечатка d.")
        col1, col2, col3 = st.columns(3)
        with col1: P = st.number_input("Нагрузка P, кгс:", min_value=100, max_value=3000, value=3000, step=100)
        with col2: D = st.number_input("Диаметр шарика D, мм:", min_value=1.0, max_value=10.0, value=10.0, step=0.5)
        with col3: d = st.number_input("Диаметр отпечатка d, мм:", min_value=1.0, max_value=9.0, value=4.0, step=0.1)
        
        HB = (2 * P) / (np.pi * D * (D - np.sqrt(D**2 - d**2)))
        st.success(f"### 📊 Твёрдость по Бринеллю: **HB = {HB:.1f} кгс/мм²**")
        
        fig_brinell = go.Figure()
        theta = np.linspace(0, 2*np.pi, 100)
        fig_brinell.add_trace(go.Scatter(x=D*np.cos(theta), y=D*np.sin(theta), fill='toself', fillcolor='lightgray', line=dict(color='gray', width=2), name='Образец'))
        fig_brinell.add_trace(go.Scatter(x=(d/2)*np.cos(theta), y=(d/2)*np.sin(theta), fill='toself', fillcolor='lightcoral', line=dict(color='red', width=3), name=f'Отпечаток d={d} мм'))
        fig_brinell.add_trace(go.Scatter(x=[-d/2, d/2], y=[0, 0], mode='lines', line=dict(color='red', width=2, dash='dash'), showlegend=False))
        fig_brinell.add_annotation(x=0, y=0.5, text=f"d = {d} мм", showarrow=False, font=dict(color='red', size=12))
        fig_brinell.update_layout(xaxis_title="мм", yaxis_title="мм", height=400, showlegend=True, title="Вид сверху: отпечаток шарика", xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(scaleanchor="x", scaleratio=1))
        st.plotly_chart(fig_brinell, use_container_width=True)
        st.markdown(f"**Формула:** HB = 2P / (πD(D - √(D²-d²)))\n\n**Подстановка:** HB = 2×{P} / (π×{D}×({D} - √({D}²-{d}²))) = **{HB:.1f} кгс/мм²**\n\n**Применение:** Для мягких и средних сталей, чугунов, цветных металлов.")

    elif method == "По Роквеллу (HRC/HRB)":
        st.markdown("#### 🔴 Метод Роквелла")
        st.markdown("**Суть:** Вдавливание алмазного конуса (HRC) или стального шарика (HRB). Измеряется глубина отпечатка h.")
        scale = st.radio("Шкала:", ["HRC (алмазный конус, твёрдые стали)", "HRB (стальной шарик, мягкие стали)"])
        col1, col2 = st.columns(2)
        with col1: P0 = st.number_input("Предварительная нагрузка P₀, кгс:", value=10)
        with col2: P1 = st.number_input("Основная нагрузка P₁, кгс:", value=140 if scale == "HRC" else 90)
        h = st.number_input("Глубина отпечатка h, мм:", min_value=0.01, max_value=0.5, value=0.1, step=0.01)
        
        if scale == "HRC":
            HR = 100 - h / 0.002
            st.success(f"### 📊 Твёрдость по Роквеллу: **HRC = {HR:.1f}**")
        else:
            HR = 130 - h / 0.002
            st.success(f"### 📊 Твёрдость по Роквеллу: **HRB = {HR:.1f}**")
            
        fig_rockwell = go.Figure()
        if scale == "HRC":
            fig_rockwell.add_trace(go.Scatter(x=[0, -0.5, 0.5, 0], y=[0, 1, 1, 0], fill='toself', fillcolor='lightyellow', line=dict(color='orange', width=2), name='Алмазный конус 120°'))
        else:
            theta = np.linspace(0, 2*np.pi, 100)
            fig_rockwell.add_trace(go.Scatter(x=0.5*np.cos(theta), y=0.5*np.sin(theta)+0.5, fill='toself', fillcolor='lightblue', line=dict(color='blue', width=2), name='Стальной шарик 1/16"'))
        fig_rockwell.add_trace(go.Scatter(x=[0, 0], y=[0, -h*10], mode='lines', line=dict(color='red', width=3), name=f'Глубина h={h} мм'))
        fig_rockwell.add_trace(go.Scatter(x=[-0.5, 0.5], y=[-h*10, -h*10], mode='lines', line=dict(color='gray', width=2), name='Образец'))
        fig_rockwell.update_layout(xaxis_title="мм", yaxis_title="мм", height=400, showlegend=True, title="Схема измерения по Роквеллу")
        st.plotly_chart(fig_rockwell, use_container_width=True)
        st.markdown(f"**Формула:** HR = {100 if scale == 'HRC' else 130} - h/0.002\n\n**Подстановка:** HR = {100 if scale == 'HRC' else 130} - {h}/0.002 = **{HR:.1f}**\n\n**Применение:** HRC для закалённых сталей, HRB для мягких сталей и цветных металлов.")

    else:
        st.markdown("#### 🟢 Метод Виккерса")
        st.markdown("**Суть:** Вдавливание алмазной четырёхгранной пирамиды. Измеряется диагональ отпечатка d.")
        col1, col2 = st.columns(2)
        with col1: P_v = st.number_input("Нагрузка P, кгс:", min_value=1, max_value=100, value=30, step=5)
        with col2: d_v = st.number_input("Диагональ отпечатка d, мм:", min_value=0.1, max_value=2.0, value=0.5, step=0.05)
        
        HV = 1.854 * P_v / (d_v ** 2)
        st.success(f"### 📊 Твёрдость по Виккерсу: **HV = {HV:.1f} кгс/мм²**")
        
        fig_vickers = go.Figure()
        fig_vickers.add_trace(go.Scatter(x=[-1, 1, 1, -1, -1], y=[-1, -1, 1, 1, -1], fill='toself', fillcolor='lightgray', line=dict(color='gray', width=2), name='Образец'))
        fig_vickers.add_trace(go.Scatter(x=[0, d_v/2, 0, -d_v/2, 0], y=[d_v/2, 0, -d_v/2, 0, d_v/2], fill='toself', fillcolor='lightgreen', line=dict(color='green', width=3), name=f'Отпечаток d={d_v} мм'))
        fig_vickers.add_trace(go.Scatter(x=[-d_v/2, d_v/2], y=[0, 0], mode='lines', line=dict(color='red', width=2, dash='dash'), showlegend=False))
        fig_vickers.add_annotation(x=0, y=0.3, text=f"d = {d_v} мм", showarrow=False, font=dict(color='red', size=12))
        fig_vickers.update_layout(xaxis_title="мм", yaxis_title="мм", height=400, showlegend=True, title="Вид сверху: отпечаток пирамиды", xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(scaleanchor="x", scaleratio=1))
        st.plotly_chart(fig_vickers, use_container_width=True)
        st.markdown(f"**Формула:** HV = 1.854 × P / d²\n\n**Подстановка:** HV = 1.854 × {P_v} / {d_v}² = **{HV:.1f} кгс/мм²**\n\n**Применение:** Универсальный метод для всех материалов, включая тонкие покрытия.")

    st.markdown("---")
    st.markdown("### 📝 Задания по твёрдости")
    st.info("💡 **Задание 1:** Почему для закалённой стали 45 используют метод Роквелла (HRC), а не Бринелля? **Подсказка:** Что произойдёт со стальным шариком при измерении очень твёрдого материала?")
    st.info("💡 **Задание 2:** Учащийся измерил твёрдость образца и получил HB = 220. Какая это примерно сталь? **Подсказка:** Посмотрите таблицу ниже.")
    st.info("💡 **Задание 3:** Почему метод Виккерса называют универсальным? **Подсказка:** Какой индентор используется и для каких материалов он подходит?")

# ==========================================
# ВКЛАДКА 4: AI-ПОМОЩНИК
# ==========================================
with tab4:
    st.markdown("### 🤖 AI-помощник по материаловедению")
    st.markdown("Персональный консультант для учащихся")
    st.markdown("---")
    
    st.markdown("""
    ## 📱 Telegram-бот "ТехноАссистент"
    
    Ваш персональный AI-помощник по материаловедению доступен 24/7 в Telegram!
    
    **Что умеет бот:**
    - 🔍 **Расшифровка марок сталей** — сфотографируйте клеймо на металле, и бот мгновенно расскажет о свойствах.
    - 📚 **Объяснение тем с нуля** — кристаллические решётки, фазовые превращения, термическая обработка.
    - 🧮 **Помощь с решением задач** — пошаговый разбор с калькулятором.
    - 📝 **Разноуровневое тестирование** — проверка знаний от простого к сложному.
    - 🔬 **Помощь с лабораторными работами** — методички, инструкции, отчёты.
    
    **Как начать:**
    1. Откройте Telegram на телефоне или компьютере.
    2. Нажмите на кнопку ниже.
    3. Нажмите "Запустить" (/start).
    4. Задайте любой вопрос по материаловедению!
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Ссылка на бота")
    
    bot_link = "https://t.me/TechnoAssistant_bot"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <a href="{bot_link}" target="_blank" style="background-color: #0088cc; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; font-size: 20px; font-weight: bold; display: inline-block; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            📱 Открыть бота в Telegram
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 Примеры запросов для бота")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔩 Расшифровка марок:**
        - "Что такое сталь 40Х?"
        - "Расшифруй марку СЧ20"
        - "Какие свойства у алюминия АМг?"
        
        **📚 Теория:**
        - "Объясни диаграмму Fe-C"
        - "Что такое аустенит?"
        - "Расскажи про закалку стали"
        """)
    with col2:
        st.markdown("""
        **🧮 Задачи:**
        - "Помоги решить задачу на твёрдость по Бринеллю"
        - "Как рассчитать предел прочности?"
        
        **📝 Тесты:**
        - "Пройди тест по кристаллическим решёткам"
        - "Проверь мои знания по термической обработке"
        """)
    
    st.markdown("---")
    st.markdown("### 🌟 Интеграция с виртуальной лабораторией")
    st.info("""
    **Как использовать бота вместе с лабораторией:**
    1. **Изучаете тему** в виртуальной лаборатории (вкладки 1-3).
    2. **Возник вопрос?** Открываете бота и спрашиваете.
    3. **Нужна помощь с задачей?** Бот пошагово разберёт решение.
    4. **Хотите проверить знания?** Бот проведёт тестирование.
    
    Это создаёт **единую образовательную экосистему**: теория + практика + персональная поддержка 24/7!
    """)

st.markdown("---")
st.caption("📖 Интерактивная виртуальная лаборатория | Кабинет материаловедения")