import os
from dotenv import load_dotenv

# Load environment variables
# load_dotenv()
# Don't use load_dotenv in Docker unless you need a local .env for dev

# API Configuration
API_BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")

# API Endpoints
ENDPOINTS = {
    "kpi": f"{API_BASE_URL}/api/v1/statistics/kpi",
    "borrowing_trends": f"{API_BASE_URL}/api/v1/statistics/borrowing-trends",
    "categories": f"{API_BASE_URL}/api/v1/statistics/categories",
    "popular_books": f"{API_BASE_URL}/api/v1/statistics/popular-books",
    "student_activity": f"{API_BASE_URL}/api/v1/statistics/student-activity",
    "overdue": f"{API_BASE_URL}/api/v1/statistics/overdue",
    "library_utilization": f"{API_BASE_URL}/api/v1/statistics/library-utilization",
    "category_trends": f"{API_BASE_URL}/api/v1/statistics/category-trends",
    "daily": f"{API_BASE_URL}/api/v1/statistics/daily",
    "copies": f"{API_BASE_URL}/api/v1/book_copies/?limit=9999",
    "books": f"{API_BASE_URL}/api/v1/book/?limit=9999",
    "metadata/locations": f"{API_BASE_URL}/api/v1/metadata/locations",
    "students": f"{API_BASE_URL}/api/v1/student",
    "student/search":f"{API_BASE_URL}/api/v1/student/search",
    "create_book": f"{API_BASE_URL}/api/v1/book/",
    "create_book_copy": f"{API_BASE_URL}/api/v1/book_copies/",
    "search_book_by_title": f"{API_BASE_URL}/api/v1/book/search/title",
    "search_author_by_name": f"{API_BASE_URL}/api/v1/metadata/authors/search",
    "create_author": f"{API_BASE_URL}/api/v1/metadata/authors/",
    "search_publisher_by_name": f"{API_BASE_URL}/api/v1/metadata/publishers/search",
    "create_publisher": f"{API_BASE_URL}/api/v1/metadata/publishers/",
    "search_location_by_name": f"{API_BASE_URL}/api/v1/metadata/locations/search",
    "create_location": f"{API_BASE_URL}/api/v1/metadata/locations/",
    "author": f"{API_BASE_URL}/api/v1/metadata/authors/?skip=0&limit=100",
}

# Category ID mapping
CATEGORY_ID_MAPPING = {
    "Class 000 - Computer science, information, and general works": 1,
    "Class 100 - Philosophy and psychology": 2,
    "Class 200 - Religion": 3,
    "Class 300 - Social sciences": 4,
    "Class 400 - Language": 5,
    "Class 500 - Science": 6,
    "Class 600 - Technology": 7,
    "Class 700 - Arts and recreation": 8,
    "Class 800 - Literature": 9,
    "Class 900 - History and geography": 10,
}

# Language code mapping
LANGUAGE_CODE_MAPPING = {
    "English": "eng",
    "Chinese": "chi",
    "Japanese": "jpn",
    "Korean": "kor",
    "Malay": "mal",
    "Tamil": "tam",
    "Spanish": "spa",
    "French": "fre",
    "German": "ger",
    "Russian": "rus",
}

# Acquisition type mapping
ACQUISITION_TYPE_MAPPING = {
    "purchased": "purchased",
    "donated": "donated",
}

# Book condition mapping
BOOK_CONDITION_MAPPING = {
    "new": "new",
    "good": "good",
    "fair": "fair",
    "poor": "poor",
    "damaged": "damaged",
}

# Book status mapping
BOOK_STATUS_MAPPING = {
    "available": "available",
    "borrowed": "borrowed",
    "missing": "missing",
    "unpublished": "unpublished",
    "disposed": "disposed",
}

# Book Location Area mapping
BOOK_LOCATION_AREA_MAPPING = {
    "Main Shelf A": 1,
    "Main Shelf B": 2,
    "Main Shelf C": 3,
    "Reference Book Area": 4,
    "Journal Area": 5,
    "New Book Display Area": 6,
    "Special Collection Area": 7,
    "Computer Science Area": 8,
    "Medical Area": 9,
    "Study Room A": 10,
    "Study Room B": 11,
    "Electronic Resource Area": 12,
    "Children's Book Area": 13,
    "Foreign Language Book Area": 14,
    "Ancient Book Area": 15,
    "Multimedia Area": 16,
    "Self-Study Room": 17,
    "Discussion Room": 18,
    "Reading Room": 19,
    "Exhibition Area": 20,
}

# 🎨 现代化配色方案 - 基于 Tailwind CSS 色彩系统
MODERN_COLORS = {
    # 主要色彩
    "primary": "#2563EB",      # 靛蓝（主要操作）
    "secondary": "#10B981",    # 绿色（次要操作）
    "accent": "#0EA5E9",       # 天蓝（强调色）
    "purple": "#4F46E5",       # 靛紫（特殊数据）
    
    # 功能性色彩
    "success": "#10B981",      # 成功状态
    "warning": "#F59E0B",      # 警告状态
    "danger": "#EF4444",       # 危险状态
    "info": "#0EA5E9",         # 信息提示
    
    # 图表专用色彩
    "chart_trend": "#9CA3AF",  # 趋势线（中灰）
    "chart_average": "#F59E0B", # 平均线（琥珀）
    
    # 饼图色彩方案（和谐互补色）
    "pie_colors": [
        "#60A5FA",  # English - 浅蓝
        "#FBBF24",  # Philosophy - 琥珀
        "#F472B6",  # Religion - 粉红
        "#34D399",  # Education - 绿色
        "#A78BFA",  # Programming - 淡紫
        "#FB7185",  # Science - 珊瑚红
        "#60A5FA",  # History - 浅蓝（变体）
        "#FCD34D",  # Art - 金黄
        "#6EE7B7",  # Medicine - 薄荷绿
        "#C084FC"   # Others - 紫色
    ],
    
    # 文字色彩
    "text_primary": "#1F2937",    # 主要文字（深灰）
    "text_secondary": "#6B7280",  # 次要文字（中灰）
    "text_muted": "#9CA3AF",      # 辅助文字（浅灰）
    "text_white": "#FFFFFF",      # 白色文字
    
    # 背景色彩
    "bg_primary": "#F9FAFB",      # 主背景（极浅灰）
    "bg_secondary": "#F3F4F6",    # 次背景（浅灰）
    "bg_white": "#FFFFFF",        # 纯白背景
    "bg_card": "#FFFFFF",         # 卡片背景
    
    # 边框与分割线
    "border_light": "#E5E7EB",    # 浅边框
    "border_medium": "#D1D5DB",   # 中等边框
    "border_dark": "#9CA3AF",     # 深边框
}

# Dashboard Configuration - 现代化主题
DASHBOARD_CONFIG = {
    "title": "Smart Library Analytics Dashboard",
    "theme": {
        "primary_color": MODERN_COLORS["primary"],
        "secondary_color": MODERN_COLORS["secondary"],
        "success_color": MODERN_COLORS["success"],
        "warning_color": MODERN_COLORS["warning"],
        "danger_color": MODERN_COLORS["danger"],
        "text_color": MODERN_COLORS["text_primary"],
        "bg_color": MODERN_COLORS["bg_primary"]
    }
}

# Cache Configuration
CACHE_CONFIG = {
    "ttl": 300  # 5 minutes
}

# 现代化图表配置
CHART_CONFIG = {
    "template": "plotly_white",
    "height": 400,
    "font_family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
    "colors": MODERN_COLORS,
    
    # 图表通用样式
    "common_layout": {
        "paper_bgcolor": MODERN_COLORS["bg_white"],
        "plot_bgcolor": MODERN_COLORS["bg_white"],
        "font": {
            "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif",
            "size": 12,
            "color": MODERN_COLORS["text_primary"]
        },
        "title": {
            "font": {
                "size": 18,
                "color": MODERN_COLORS["text_primary"],
                "family": "Inter, -apple-system, BlinkMacSystemFont, sans-serif"
            },
            "x": 0.5,
            "xanchor": "center"
        },
        "margin": {"l": 60, "r": 60, "t": 80, "b": 60}
    },
    
    # 网格样式
    "grid_style": {
        "showgrid": True,
        "gridcolor": MODERN_COLORS["border_light"],
        "gridwidth": 1,
        "zeroline": True,
        "zerolinecolor": MODERN_COLORS["border_medium"],
        "zerolinewidth": 1
    },
    
    # 图例样式
    "legend_style": {
        "bgcolor": "rgba(255,255,255,0.95)",
        "bordercolor": MODERN_COLORS["border_light"],
        "borderwidth": 1,
        "font": {
            "size": 11,
            "color": MODERN_COLORS["text_primary"]
        }
    }
}

# ===========================================
# 2. 更新主文件的 CSS 样式
# ===========================================

MODERN_CSS = """
<style>
    /* 导入现代字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* 全局字体设置 */
    .main, .sidebar, .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #F9FAFB !important;
    }
    
    /* 现代化指标卡片 */
    .metric-card {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        padding: 1.5rem !important;
        border-radius: 12px !important;
        color: white !important;
        text-align: center !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        border: none !important;
    }
    
    /* 指标文字样式 */
    .stMetric > label {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #6B7280 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    .stMetric > div {
        font-size: 24px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
    }
    
    /* 现代化主标题 */
    .main-header {
        text-align: center !important;
        padding: 2.5rem 0 !important;
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border-radius: 16px !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    
    .main-header h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
    }
    
    .main-header p {
        font-size: 1.1rem !important;
        opacity: 0.9 !important;
        font-weight: 400 !important;
    }
    
    /* 现代化章节标题 */
    .section-header {
        border-left: 4px solid #2563EB !important;
        padding-left: 1rem !important;
        margin: 2rem 0 1.5rem 0 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #1F2937 !important;
        background-color: #F9FAFB !important;
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* 现代化错误和成功消息 */
    .error-message {
        padding: 1rem 1.5rem !important;
        background-color: #FEF2F2 !important;
        border-left: 4px solid #EF4444 !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
        color: #DC2626 !important;
        font-weight: 500 !important;
    }
    
    .success-message {
        padding: 1rem 1.5rem !important;
        background-color: #ECFDF5 !important;
        border-left: 4px solid #10B981 !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
        color: #059669 !important;
        font-weight: 500 !important;
    }
    
    /* 侧边栏现代化 */
    .css-1d391kg {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
    }
    
    /* 现代化按钮 */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
        transform: translateY(-1px) !important;
    }
    
    /* 现代化选择框 */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 8px !important;
        color: #1F2937 !important;
    }
    
    /* 现代化数据表格 */
    .stDataFrame {
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    /* 现代化展开器 */
    .streamlit-expanderHeader {
        background-color: #F3F4F6 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 8px !important;
        color: #1F2937 !important;
        font-weight: 600 !important;
    }
    
    /* 隐藏Streamlit默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 图表容器现代化 */
    .js-plotly-plot {
        border-radius: 12px !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
        background-color: #FFFFFF !important;
    }
</style>
"""