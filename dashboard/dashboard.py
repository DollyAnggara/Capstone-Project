import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from pathlib import Path
import ast

sns.set(style='dark')


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


def parse_city(value):
    """Ambil nama kota dari kolom lokasi."""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        return text.split(',')[0].strip()
    return None

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

def get_city_job_count(df):
    """Mendapatkan jumlah lowongan per kota"""
    if 'city' in df.columns:
        city_counts = df['city'].value_counts().head(15)
        return city_counts.sort_values(ascending=True)
    return pd.Series()

def get_city_top_salary(df):
    """Mendapatkan kota dengan rata-rata gaji tertinggi"""
    if 'city' in df.columns and 'salary' in df.columns:
        city_avg_salary = df.groupby('city')['salary'].mean().sort_values(ascending=True).tail(10)
        return city_avg_salary
    return pd.Series()

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

if 'city' not in main_data.columns and 'location' in main_data.columns:
    main_data['city'] = main_data['location'].apply(parse_city)

if 'city' in main_data.columns:
    main_data['city'] = main_data['city'].apply(parse_city)

# ==================== TAMPILAN DASHBOARD ====================

st.header('Dashboard Analisis Pasar Kerja ')
st.markdown('Dashboard ini menyajikan analisis pasar kerja berdasarkan skill yang dicari, distribusi gaji, dan lokasi pekerjaan.')

# ==================== VISUALISASI 1: TOP SKILLS ====================
st.subheader(' Top Skills yang Paling Sering Dicari')

top_skills = get_top_skills(main_data)

if top_skills:
    fig, ax = plt.subplots(figsize=(12, 8))
    skills_names = list(top_skills.keys())
    skills_values = list(top_skills.values())
    
    colors = plt.cm.viridis([i/len(skills_names) for i in range(len(skills_names))])
    bars = ax.barh(skills_names, skills_values, color=colors)
    
    ax.set_xlabel('Jumlah Lowongan', fontsize=12)
    ax.set_ylabel('Skill', fontsize=12)
    ax.set_title(f'Top {len(top_skills)} Skill yang Paling Sering Dicari', fontsize=14, fontweight='bold')
    
    # Tambahkan label nilai
    for bar, val in zip(bars, skills_values):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2,
                str(val), va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("Data skills tidak tersedia")

# ==================== VISUALISASI 2: SKILL PER INDUSTRI ====================
st.subheader('Top Skill per Industri')

skills_by_industry = get_skills_by_industry(main_data)

if skills_by_industry:
    industries_list = [i for i in skills_by_industry.keys() if skills_by_industry[i]]
    industries_to_show = industries_list[:6]

    if industries_to_show:
        n_cols = 3
        n_rows = (len(industries_to_show) + n_cols - 1) // n_cols
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 4 * n_rows))
        axes = axes.flatten() if hasattr(axes, 'flatten') else [axes]

        color_map = plt.cm.Set2
        for idx, industry in enumerate(industries_to_show):
            ax = axes[idx]
            top_items = skills_by_industry[industry]
            skills = [item[0] for item in top_items][::-1]
            counts = [item[1] for item in top_items][::-1]

            bars = ax.barh(skills, counts, color=color_map(idx % 8))
            ax.set_title(industry, fontsize=12, fontweight='bold')
            ax.set_xlabel('Jumlah', fontsize=10)

            for bar, val in zip(bars, counts):
                ax.text(bar.get_width() + max(counts) * 0.02, bar.get_y() + bar.get_height() / 2,
                        str(val), va='center', fontsize=8)

        for idx in range(len(industries_to_show), len(axes)):
            axes[idx].axis('off')

        fig.suptitle('Top Skill per Industri', fontsize=16, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Data skill per industri tidak tersedia")
else:
    st.info("Data skill per industri tidak tersedia")

# ==================== VISUALISASI 3: GAJI PER INDUSTRI ====================
st.subheader('Distribusi Gaji Berdasarkan Industri')

avg_salary = get_avg_salary_by_industry(main_data)

if not avg_salary.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        industries = avg_salary.index
        salaries = avg_salary.values
        
        colors = plt.cm.viridis([i/len(industries) for i in range(len(industries))])
        bars = ax.barh(industries, salaries, color=colors)
        
        ax.set_title('Rata-rata Gaji per Kategori Industri', fontsize=14, fontweight='bold')
        ax.set_xlabel('Rata-rata Gaji (USD)', fontsize=12)
        ax.set_ylabel('Industri', fontsize=12)
        
        for bar, val in zip(bars, salaries):
            ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height()/2,
                    f'${val:,.0f}', va='center', fontsize=10)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.metric("Industri dengan Gaji Tertinggi", avg_salary.index[-1], 
                  f"${avg_salary.values[-1]:,.0f}")
        st.metric("Industri dengan Gaji Terendah", avg_salary.index[0],
                  f"${avg_salary.values[0]:,.0f}")
        st.metric("Rata-rata Gaji Keseluruhan", f"${avg_salary.mean():,.0f}")
else:
    st.warning("Data gaji tidak tersedia")


# ==================== INSIGHT KESIMPULAN ====================
st.subheader('Insight & Kesimpulan')

insights = [
    "**Skill Teknis Mendominasi**: Python dan SQL adalah skill yang paling banyak dicari.",
    "**Industri Teknologi dan Software** memiliki kebutuhan skill programming yang tinggi.",
    "**Gaji Antar Industri** relatif merata dengan selisih tidak terlalu signifikan.",
]

for insight in insights:
    st.markdown(f"- {insight}")

