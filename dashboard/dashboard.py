import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from pathlib import Path
import ast
import numpy as np

sns.set_theme(style='whitegrid', context='talk')

st.set_page_config(
    page_title='Dashboard Analisis Pasar Kerja',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='collapsed',
)


def inject_styles():
    st.markdown(
        '''
        <style>
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(245, 158, 11, 0.12), transparent 30%),
                    radial-gradient(circle at top right, rgba(34, 197, 94, 0.10), transparent 24%),
                    linear-gradient(180deg, #fffdf8 0%, #f8f5ef 100%);
                color: #1f2937;
            }

            .main .block-container {
                padding-top: 1.2rem;
                padding-bottom: 2rem;
            }

            .hero-card {
                padding: 1.8rem 2rem;
                border-radius: 28px;
                background: linear-gradient(135deg, #1f2937 0%, #3f2d20 55%, #8a4b12 100%);
                color: #fff7ed;
                box-shadow: 0 24px 60px rgba(31, 41, 55, 0.20);
                border: 1px solid rgba(255, 255, 255, 0.08);
            }

            .hero-card h1 {
                margin: 0;
                font-size: 2.15rem;
                line-height: 1.1;
                color: #fffaf3;
            }

            .hero-card p {
                margin-top: 0.75rem;
                margin-bottom: 0;
                color: rgba(255, 250, 243, 0.88);
                font-size: 1rem;
            }

            .section-card {
                background: rgba(255, 255, 255, 0.90);
                border: 1px solid rgba(120, 113, 108, 0.15);
                border-radius: 24px;
                padding: 1.2rem 1.2rem 0.9rem 1.2rem;
                box-shadow: 0 12px 28px rgba(31, 41, 55, 0.06);
                margin-bottom: 1rem;
            }

            .section-caption {
                color: #6b7280;
                font-size: 0.94rem;
                margin-top: -0.25rem;
                margin-bottom: 0.75rem;
            }

            .insight-box {
                background: linear-gradient(135deg, rgba(245,158,11,0.06), rgba(250,204,21,0.02));
                border: 1px solid rgba(245,158,11,0.12);
                border-radius: 12px;
                padding: 0.9rem 0.9rem;
                color: #1f2937;
                box-shadow: 0 8px 18px rgba(31,41,55,0.04);
            }

            .highlight-card {
                background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,252,242,0.95));
                border-radius: 12px;
                padding: 0.9rem 1rem;
                border: 1px solid rgba(148,163,184,0.06);
            }

            .highlight-card h4 { margin: 0 0 6px 0; color: #92400e; }
            .highlight-row { display:flex; flex-direction:column; gap:6px; }
            .hl-item { display:flex; justify-content:space-between; align-items:center; padding:6px 8px; border-radius:8px; background: rgba(15,23,42,0.02); }
            .hl-label { color:#6b7280; font-size:0.92rem; }
            .hl-value { color:#1f2937; font-weight:700; }

            .conclusion-grid { display:grid; grid-template-columns:repeat(3, 1fr); gap:14px; margin-top:8px; }
            .conclusion-card { background: rgba(255,255,255,0.95); padding:12px 14px; border-radius:12px; border:1px solid rgba(148,163,184,0.06); box-shadow:0 8px 18px rgba(31,41,55,0.04); }
            .conclusion-card h4 { margin:0 0 6px 0; color:#92400e; }
            .conclusion-card p { margin:0; color:#374151; font-size:0.95rem; }
            }

            h1, h2, h3 {
                color: #1f2937;
                letter-spacing: -0.02em;
            }

            .stMarkdown, .stText, .stMetric, .stDataFrame, .stInfo, .stWarning {
                color: #1f2937;
            }

            div[data-testid='stMetric'] {
                background: rgba(255, 255, 255, 0.90);
                border: 1px solid rgba(120, 113, 108, 0.15);
                border-radius: 18px;
                padding: 0.9rem 0.95rem;
                box-shadow: 0 10px 22px rgba(31, 41, 55, 0.05);
            }

            div[data-testid='stMetric'] * {
                color: #1f2937 !important;
            }

            [data-testid='stTabs'] button {
                border-radius: 999px;
                padding: 0.35rem 0.95rem;
                margin-right: 0.35rem;
                color: #1f2937;
            }

            [data-testid='stTabs'] button[aria-selected='true'] {
                background: rgba(245, 158, 11, 0.18);
                color: #7c2d12;
            }

            .stSelectbox label, .stDataFrame label {
                color: #1f2937;
            }
        </style>
        ''',
        unsafe_allow_html=True,
    )


inject_styles()


def parse_skills(value):
    """Normalisasi nilai skills_list menjadi list string."""
    if isinstance(value, list):
        return [str(s).strip() for s in value if str(s).strip()]

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return []

        if text.startswith('[') and text.endswith(']'):
            try:
                parsed = ast.literal_eval(text)
                if isinstance(parsed, list):
                    return [str(s).strip() for s in parsed if str(s).strip()]
            except (ValueError, SyntaxError):
                pass

        return [s.strip() for s in text.split(',') if s.strip()]

    return []


def format_usd(value):
    if pd.isna(value):
        return '-'
    return format_currency(float(value), 'USD', locale='en_US')


def chart_frame(ax, title, xlabel='', ylabel=''):
    ax.set_title(title, loc='left', pad=16, fontsize=16, fontweight='bold', color='#1f2937')
    ax.set_xlabel(xlabel, fontsize=11, color='#374151')
    ax.set_ylabel(ylabel, fontsize=11, color='#374151')
    ax.grid(axis='x', linestyle='--', alpha=0.22, color='#a8a29e')
    ax.set_axisbelow(True)
    ax.set_facecolor('#ffffff')

    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_alpha(0.22)
    ax.spines['bottom'].set_alpha(0.22)


def annotate_bars(ax, bars, values, fmt='{:,}', offset_ratio=0.018):
    if not values:
        return

    max_value = max(values)
    offset = max_value * offset_ratio if max_value else 0.5
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_width() + offset,
            bar.get_y() + bar.get_height() / 2,
            fmt.format(value),
            va='center',
            ha='left',
            fontsize=9,
            color='#1f2937',
        )


# ==================== FUNGSI ANALISIS ====================

def get_top_skills(df, n=20):
    """Mendapatkan top N skills yang paling sering dicari"""
    all_skills = []
    
    if 'skills_list' in df.columns:
        for skills in df['skills_list'].dropna():
            if isinstance(skills, list):
                all_skills.extend(skills)
            elif isinstance(skills, str):
                all_skills.extend([s.strip() for s in skills.split(',')])
    
    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = dict(skill_counts.most_common(n))
    
    # Balik urutan untuk tampilan
    return {k: top_skills[k] for k in list(top_skills.keys())[::-1]}


def get_top_industries(df, n=8):
    if 'category' not in df.columns:
        return pd.Series(dtype=int)

    return df['category'].value_counts().head(n).sort_values(ascending=True)

def get_skills_by_industry(df, n=10):
    """Mendapatkan top N skill beserta jumlahnya untuk tiap industri"""
    if 'category' not in df.columns or 'skills_list' not in df.columns:
        return {}
    
    from collections import Counter
    industry_skills = {}
    for industry in df['category'].unique():
        industry_df = df[df['category'] == industry]
        all_skills = []
        for skills in industry_df['skills_list'].dropna():
            all_skills.extend(parse_skills(skills))
        skill_counts = Counter(all_skills)
        industry_skills[industry] = skill_counts.most_common(n)
    
    return industry_skills

def get_avg_salary_by_industry(df):
    """Mendapatkan rata-rata gaji per industri"""
    if 'category' in df.columns and 'salary' in df.columns:
        avg_salary = df.groupby('category')['salary'].mean().sort_values(ascending=True)
        return avg_salary
    return pd.Series()


def get_top_skills_by_salary(df, n=10, min_occurrences=50):
    """Mendapatkan top N skill dengan gaji rata-rata tertinggi"""
    if 'skills_list' not in df.columns or 'salary' not in df.columns:
        return pd.DataFrame()
    
    skill_salary_data = []
    for idx, row in df.iterrows():
        skills_list = row['skills_list']
        salary = row['salary']
        if isinstance(skills_list, list) and len(skills_list) > 0:
            for skill in skills_list:
                skill_salary_data.append({'skill': skill, 'salary': salary})
    
    if not skill_salary_data:
        return pd.DataFrame()
    
    skill_salary_df = pd.DataFrame(skill_salary_data)
    top_skills = skill_salary_df.groupby('skill')['salary'].agg(['mean', 'count']).sort_values(by='mean', ascending=False).head(n)
    
    # Filter hanya skill yang muncul minimal min_occurrences kali (untuk akurasi)
    top_skills = top_skills[top_skills['count'] >= min_occurrences]
    
    return top_skills.sort_values(by='mean', ascending=True)


def get_dashboard_metrics(df):
    return {
        'total_jobs': len(df),
        'total_companies': df['company'].nunique() if 'company' in df.columns else 0,
        'total_categories': df['category'].nunique() if 'category' in df.columns else 0,
        'skills_mentions': int(sum(len(skills) for skills in df['skills_list'])) if 'skills_list' in df.columns else 0,
        'avg_salary': df['salary'].mean() if 'salary' in df.columns else pd.NA,
    }


# ==================== MEMUAT DATA ====================
def load_data():
    """Memuat dataset all_jobs_data.csv"""
    try:
        data_path = Path(__file__).resolve().parent / "all_jobs_data.csv"
        df = pd.read_csv(data_path)
        return df
    except FileNotFoundError:
        st.error(f"File all_jobs_data.csv tidak ditemukan di: {data_path}")
        st.stop()

main_data = load_data()

# Preprocessing data
if 'salary' in main_data.columns:
    main_data['salary'] = pd.to_numeric(main_data['salary'], errors='coerce')

if 'skills_list' in main_data.columns:
    main_data['skills_list'] = main_data['skills_list'].apply(parse_skills)

# ==================== TAMPILAN DASHBOARD ====================

dashboard_metrics = get_dashboard_metrics(main_data)

st.markdown(
    '''
    <div class="hero-card">
        <h1>Dashboard Analisis Pasar Kerja</h1>
    </div>
    ''',
    unsafe_allow_html=True,
)

st.write('')

metric_cols = st.columns(5)
metric_values = [
    ('Total Lowongan', f"{dashboard_metrics['total_jobs']:,}"),
    ('Perusahaan', f"{dashboard_metrics['total_companies']:,}"),
    ('Industri', f"{dashboard_metrics['total_categories']:,}"),
    ('Mentions Skill', f"{dashboard_metrics['skills_mentions']:,}"),
    ('Rata-rata Gaji', format_usd(dashboard_metrics['avg_salary'])),
]

for col, (label, value) in zip(metric_cols, metric_values):
    with col:
        st.metric(label, value)

st.write('')

tab_overview, tab_skills, tab_salary = st.tabs(['Ringkasan', 'Skill', 'Gaji'])

with tab_overview:
    st.subheader('Ringkasan Pasar Kerja')
    st.markdown(
        '<div class="section-caption">Dua grafik berikut menampilkan skill yang paling dicari dan industri dengan jumlah lowongan terbesar.</div>',
        unsafe_allow_html=True,
    )

    overview_left, overview_right = st.columns([1, 1])

    top_skills = get_top_skills(main_data, n=15)
    with overview_left:
        if top_skills:
            fig, ax = plt.subplots(figsize=(10.8, 7.2), facecolor='white')
            skills_names = list(top_skills.keys())
            skills_values = list(top_skills.values())
            palette = sns.color_palette('YlOrBr', n_colors=len(skills_names))
            bars = ax.barh(skills_names, skills_values, color=palette, edgecolor='white', linewidth=0.8)
            chart_frame(ax, f'Top {len(top_skills)} Skill yang Paling Dicari', 'Jumlah Lowongan', 'Skill')
            annotate_bars(ax, bars, skills_values)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
        else:
            st.warning('Data skills tidak tersedia')

    with overview_right:
        top_industries = get_top_industries(main_data, n=8)
        if not top_industries.empty:
            fig, ax = plt.subplots(figsize=(10.8, 7.2), facecolor='white')
            industries = list(top_industries.index)
            counts = list(top_industries.values)
            bars = ax.barh(industries, counts, color=sns.color_palette('rocket', n_colors=len(industries)), edgecolor='white', linewidth=0.8)
            chart_frame(ax, 'Industri dengan Volume Lowongan Terbesar', 'Jumlah Lowongan', 'Industri')
            annotate_bars(ax, bars, counts)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)
        else:
            st.info('Data industri tidak tersedia')

with tab_skills:
    st.subheader('Skill per Industri')
    st.markdown(
        '<div class="section-caption">Pilih industri untuk melihat skill paling dominan. Warna grafik dibuat hangat agar lebih mudah dibaca.</div>',
        unsafe_allow_html=True,
    )

    skills_by_industry = get_skills_by_industry(main_data)
    industries_list = [industry for industry in skills_by_industry.keys() if skills_by_industry[industry]]

    if industries_list:
        selected_industry = st.selectbox('Pilih industri', industries_list)
        selected_skill_data = skills_by_industry.get(selected_industry, [])

        if selected_skill_data:
            top_skill_name, top_skill_count = selected_skill_data[0]
            skill_names = [item[0] for item in selected_skill_data][::-1]
            skill_counts = [item[1] for item in selected_skill_data][::-1]

            skill_cols = st.columns([1.3, 0.7])
            with skill_cols[0]:
                fig, ax = plt.subplots(figsize=(11, 7), facecolor='white')
                bars = ax.barh(skill_names, skill_counts, color=sns.color_palette('flare', n_colors=len(skill_names)), edgecolor='white', linewidth=0.8)
                chart_frame(ax, f'Skill Teratas di Industri {selected_industry}', 'Jumlah Lowongan', 'Skill')
                annotate_bars(ax, bars, skill_counts)
                plt.tight_layout()
                st.pyplot(fig, clear_figure=True)

            with skill_cols[1]:
                                # Tampilkan kartu highlight yang lebih menarik
                                st.markdown(
                                        f"""
                                        <div class="highlight-card">
                                            <h4>Highlight Industri</h4>
                                            <div class="highlight-row">
                                                <div class="hl-item"><span class="hl-label">Industri</span><span class="hl-value">{selected_industry}</span></div>
                                                <div class="hl-item"><span class="hl-label">Top Skill</span><span class="hl-value">{top_skill_name}</span></div>
                                                <div class="hl-item"><span class="hl-label">Jumlah Muncul</span><span class="hl-value">{top_skill_count:,}</span></div>
                                                <div class="hl-item"><span class="hl-label">Total Skill Unik</span><span class="hl-value">{len(selected_skill_data):,}</span></div>
                                            </div>
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                )
        else:
            st.info('Data skill untuk industri terpilih tidak tersedia')
    else:
        st.info('Data skill per industri tidak tersedia')

with tab_salary:
    st.subheader('Distribusi Gaji per Industri')
    st.markdown(
        '<div class="section-caption">Bagian ini menampilkan perbandingan gaji rata-rata antar industri dengan label nilai yang jelas.</div>',
        unsafe_allow_html=True,
    )

    avg_salary = get_avg_salary_by_industry(main_data)

    if not avg_salary.empty:
        salary_left, salary_right = st.columns([1.35, 0.75])

        with salary_left:
            fig, ax = plt.subplots(figsize=(11.5, 7.5), facecolor='white')
            industries = list(avg_salary.index)
            salaries = list(avg_salary.values)
            bars = ax.barh(range(len(industries)), salaries, color=sns.color_palette('crest', n_colors=len(industries)), edgecolor='white', linewidth=0.8, height=0.7)
            
            ax.set_yticks(range(len(industries)))
            ax.set_yticklabels(industries, fontsize=10)
            chart_frame(ax, 'Rata-rata Gaji per Kategori Industri', 'Rata-rata Gaji (USD)', 'Industri')
            
            # Annotate with salary values
            for i, sal in enumerate(salaries):
                ax.text(sal + 500, i, f'${sal:,.0f}', va='center', fontsize=10, fontweight='bold', color='#1f2937')
            
            ax.set_xlim(0, 120000)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)

        with salary_right:
            top_industry = avg_salary.idxmax()
            bottom_industry = avg_salary.idxmin()
            st.markdown('**Ringkasan Gaji**')
            st.metric('Industri dengan gaji tertinggi', top_industry, format_usd(avg_salary.max()))
            st.metric('Industri dengan gaji terendah', bottom_industry, format_usd(avg_salary.min()))
            st.metric('Rata-rata gaji keseluruhan', format_usd(avg_salary.mean()))
    else:
        st.warning('Data gaji tidak tersedia')

    # Divider
    st.divider()

    # Top 10 Skills by Salary
    st.markdown('### Top 10 Skill dengan Gaji Tertinggi')
    st.markdown(
        '<div class="section-caption">"Bagian ini menunjukkan 10 Skill yang memiliki rata-rata gaji tertinggi</div>',
        unsafe_allow_html=True,
    )

    top_skills_salary = get_top_skills_by_salary(main_data, n=10, min_occurrences=50)

    if not top_skills_salary.empty:
        salary_skills_left, salary_skills_right = st.columns([1.35, 0.75])

        with salary_skills_left:
            fig, ax = plt.subplots(figsize=(11.5, 7.5), facecolor='white')
            skills_names = top_skills_salary.index.tolist()
            skills_salaries = top_skills_salary['mean'].values.tolist()
            colors = plt.cm.RdYlGn(np.linspace(0.3, 0.8, len(skills_names)))
            bars = ax.barh(range(len(skills_names)), skills_salaries, color=colors, edgecolor='white', linewidth=0.8, height=0.7)
            
            ax.set_yticks(range(len(skills_names)))
            ax.set_yticklabels(skills_names, fontsize=10)
            chart_frame(ax, 'Top 10 Skill dengan Rata-rata Gaji Tertinggi', 'Rata-rata Gaji (USD)', 'Skill')
            
            # Annotate with salary and count
            for i, (sal, count) in enumerate(zip(top_skills_salary['mean'].values, top_skills_salary['count'].values)):
                ax.text(sal + 500, i, f'${sal:,.0f} (n={int(count)})', va='center', fontsize=10, fontweight='bold', color='#1f2937')
            
            ax.set_xlim(0, 120000)
            plt.tight_layout()
            st.pyplot(fig, clear_figure=True)

        with salary_skills_right:
            top_skill_name = top_skills_salary['mean'].idxmax()
            top_skill_salary = top_skills_salary['mean'].max()
            top_skill_count = top_skills_salary.loc[top_skill_name, 'count']
            
            st.markdown('**Skill Bernilai Premium**')
            st.metric('Skill dengan gaji tertinggi', top_skill_name, format_usd(top_skill_salary))
            st.metric('Jumlah kemunculan', f"{int(top_skill_count):,}")
            st.metric('Rata-rata gaji semua skill', format_usd(top_skills_salary['mean'].mean()))
    else:
        st.info('Data skill dengan gaji tidak tersedia')

st.subheader('Insight & Kesimpulan')
insights = [
    ('Skill Teknis Mendominasi', 'Python, SQL, dan tool cloud muncul paling sering dan menjadi prioritas rekrutmen di banyak kategori.'),
    ('Industri dengan Variasi Skill', 'Industri besar (Retail, Finance, Healthcare) menunjukkan variasi skill yang tinggi.'),
    ('Gaji & Perbandingan', 'Rata-rata gaji relatif stabil di $94-96K lintas industri, namun skill dengan gaji tertinggi (C++, Market Research, Nursing) bukan yang paling populer.'),
]

cards_html = '<div class="conclusion-grid>'
cards_html = '<div class="conclusion-grid">'
for title, text in insights:
    cards_html += f'<div class="conclusion-card"><h4>{title}</h4><p>{text}</p></div>'
cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)

