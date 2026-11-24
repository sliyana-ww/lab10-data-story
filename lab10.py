import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Lab 10 | Framing the Data Story", layout="wide")

# Standardized CSS so dark mode doesn't wash out sidebar text, slider labels, or expander headers
st.markdown(
    """
    <style>
        .stApp {
            background-color: #FFF0F5;
            color: #2B111A;
        }
        [data-testid="stHeader"] {
            background-color: #FFF0F5;
            color: #2B111A;
        }
        [data-testid="stHeader"] a,
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] span,
        [data-testid="stHeader"] svg {
            color: #2B111A !important;
            fill: #2B111A !important;
            opacity: 1 !important;
        }

        /* Sidebar: white text over pink/rose sidebar */
        [data-testid="stSidebar"] {
            background-color: #D84B7A;
        }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] strong {
            color: #FFFFFF !important;
        }

        /* Slider label, ticks, and thumb value in sidebar */
        [data-testid="stSidebar"] [data-testid="stSlider"] label,
        [data-testid="stSidebar"] [data-testid="stSlider"] div,
        [data-testid="stSidebar"] [data-testid="stSlider"] span,
        [data-testid="stSidebar"] [data-testid="stTickBarMin"],
        [data-testid="stSidebar"] [data-testid="stTickBarMax"],
        [data-testid="stSidebar"] [data-testid="stThumbValue"] {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        /* Light blue slider across BaseWeb divs & SVG elements */
        [data-testid="stSlider"] [data-baseweb="slider"] div,
        [data-testid="stSlider"] [data-baseweb="slider"] span,
        [data-testid="stSlider"] [style*="background"] {
            background-color: #8FD3FF !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div > div:first-child {
            background-color: #D6ECFF !important;
        }
        [data-testid="stSlider"] [role="slider"] {
            background-color: #7CC6FE !important;
            border: 2px solid #FFFFFF !important;
            box-shadow: 0 0 0 4px rgba(124, 198, 254, 0.45) !important;
        }
        [data-testid="stSlider"] svg,
        [data-testid="stSlider"] svg rect,
        [data-testid="stSlider"] svg circle,
        [data-testid="stSlider"] svg path {
            fill: #7CC6FE !important;
            stroke: #FFFFFF !important;
        }

        /* Expander header & container with strong contrast */
        [data-testid="stExpander"] {
            background-color: #FFE4EC;
            border: 1.5px solid #C2185B;
            border-radius: 8px;
        }
        [data-testid="stExpander"] summary {
            background-color: #F8BBD0 !important;
            color: #2B111A !important;
            border-radius: 6px;
        }
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary svg {
            color: #2B111A !important;
            fill: #2B111A !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Base Data (Lesson 2) ---
base_skills = [
    "Data storytelling",
    "Python",
    "Chart selection",
    "Color and labels",
    "Data cleaning",
]
base_ratings = [2.4, 3.0, 3.2, 3.7, 4.1]

# --- Sidebar: Student Information ---
st.sidebar.subheader("Student information")
st.sidebar.markdown("**Name:** Liyana Siah")
st.sidebar.markdown("**Student ID:** 22006725")
st.sidebar.markdown("**Course:** TFB3133: Data Visualization")
st.sidebar.markdown("**Assignment:** Lab 10 – Framing the Data Story")
st.sidebar.divider()

# --- Sidebar: Story Framing Controls (Lesson 3 Tasks) ---
st.sidebar.subheader("Story Framing Controls")

audience_choice = st.sidebar.radio(
    "1. Target Audience",
    [
        "Student committee (peer workshop)",
        "Course lecturer (lab redesign)",
        "Faculty coordinator (resource allocation)",
    ],
)

modify_rating = st.sidebar.checkbox("2. Adjust a skill rating ", value=False)
selected_skill = "Chart selection"
updated_rating = 3.2

if modify_rating:
    selected_skill = st.sidebar.selectbox(
        "Skill to modify",
        base_skills,
        index=2,  # Defaults to Chart selection so you can test shifting the lowest bar
    )
    default_val = base_ratings[base_skills.index(selected_skill)]
    updated_rating = st.sidebar.slider(
        f"{selected_skill} average rating",
        min_value=1.0,
        max_value=5.0,
        value=float(default_val),
        step=0.1,
    )

highlight_mode = st.sidebar.radio(
    "3. Visual Emphasis Style",
    [
        "Contrasting color",
        "Sorted position + callout annotation",
    ],
)

# --- Build Active Dataset ---
ratings = list(base_ratings)
if modify_rating:
    skill_idx = base_skills.index(selected_skill)
    ratings[skill_idx] = updated_rating

df = pd.DataFrame({"Skill": base_skills, "Average rating": ratings})

# Sort lowest-to-highest when using position-based emphasis
if highlight_mode == "Sorted position + callout annotation":
    plot_df = df.sort_values(by="Average rating", ascending=True).reset_index(drop=True)
else:
    plot_df = df.copy()

# Identify lowest and second-lowest ratings dynamically
sorted_vals = df.sort_values(by="Average rating", ascending=True).reset_index(drop=True)
lowest_skill = sorted_vals.loc[0, "Skill"]
lowest_val = sorted_vals.loc[0, "Average rating"]
second_val = sorted_vals.loc[1, "Average rating"]
gap = round(second_val - lowest_val, 1)

# --- Audience-Specific Framing ---
if audience_choice == "Student committee (peer workshop)":
    question = "Which topic do classmates struggle with most for our upcoming peer session?"
    takeaway = (
        f"**{lowest_skill}** has the lowest average self-rating (**{lowest_val:.1f} / 5**), "
        "making it the clearest priority for peer-led practice."
    )
    chart_title = f"Focus the student workshop on {lowest_skill.lower()}"
    annotation_text = "Lowest score: top peer priority"
elif audience_choice == "Course lecturer (lab redesign)":
    question = "Where do students lack confidence, and how much scaffolding is needed?"
    takeaway = (
        f"Students average only **{lowest_val:.1f} / 5** in **{lowest_skill.lower()}**—"
        "near beginner level—indicating a need for step-by-step templates before independent tasks."
    )
    chart_title = f"Dedicate extra lab scaffolding to {lowest_skill.lower()}"
    annotation_text = "Lowest confidence: add guided examples"
else:
    question = "Which single training area delivers the highest impact for lab support funding?"
    takeaway = (
        f"**{lowest_skill}** trails the next-lowest skill by **{gap:.1f} points** "
        f"({lowest_val:.1f} vs. {second_val:.1f}), justifying targeted support over broad coverage."
    )
    chart_title = f"Allocate lab support budget to {lowest_skill.lower()}"
    annotation_text = f"Trails next skill by {gap:.1f} pts"

# --- Main Page Layout ---
st.title("Lab 10: Framing the Data Story")
st.caption("TFB3133 | Audience-focused visualisation")

col1, col2 = st.columns([1, 1.35])
with col1:
    st.markdown(f"**Audience:** {audience_choice}")
    st.markdown(f"**Decision Question:** {question}")
with col2:
    st.markdown(f"**Key Takeaway:** {takeaway}")

# --- Matplotlib Figure (Pink Palette) ---
fig, ax = plt.subplots(figsize=(8.8, 4.2))
fig.patch.set_facecolor("#FFF0F5")
ax.set_facecolor("#FFF0F5")

lowest_mask = plot_df["Average rating"] == lowest_val

if highlight_mode == "Contrasting color":
    bar_colors = ["#C2185B" if is_low else "#E5A9BC" for is_low in lowest_mask]
else:
    bar_colors = ["#F4B6C8"] * len(plot_df)

bars = ax.barh(plot_df["Skill"], plot_df["Average rating"], color=bar_colors, height=0.62)

ax.set_xlim(0, 5.7)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xlabel("Average self-rating across students (1 = beginner, 5 = confident)", fontsize=9.5, color="#2B111A")
ax.set_title(chart_title, fontsize=11.5, fontweight="bold", pad=12, color="#2B111A")
ax.invert_yaxis()

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#8E4A63")
ax.spines["bottom"].set_color("#8E4A63")
ax.tick_params(axis="both", labelsize=9, colors="#2B111A")

for idx, (bar, value, is_low) in enumerate(
    zip(bars, plot_df["Average rating"], lowest_mask)
):
    ax.text(
        value + 0.08,
        bar.get_y() + bar.get_height() / 2,
        f"{value:.1f}",
        va="center",
        ha="left",
        fontsize=9.5,
        fontweight="bold" if is_low else "normal",
        color="#880E4F" if is_low else "#2B111A",
    )

if highlight_mode == "Sorted position + callout annotation":
    for tick_label, is_low in zip(ax.get_yticklabels(), lowest_mask):
        if is_low:
            tick_label.set_fontweight("bold")
            tick_label.set_color("#880E4F")

    first_low_idx = lowest_mask.idxmax()
    target_bar = bars[first_low_idx]
    y_center = target_bar.get_y() + target_bar.get_height() / 2

    ax.annotate(
        annotation_text,
        xy=(lowest_val + 0.42, y_center),
        xytext=(3.45, y_center),
        va="center",
        ha="left",
        fontsize=9,
        fontweight="bold",
        color="#880E4F",
        arrowprops=dict(
            arrowstyle="->",
            color="#880E4F",
            lw=1.1,
            shrinkA=4,
            shrinkB=4,
        ),
    )

fig.text(
    0.01,
    0.01,
    "Fictional practice values (2026). Each bar shows the group average self-rating on a 1–5 scale.",
    fontsize=8,
    color="#6D3B4E",
)
fig.tight_layout(rect=[0, 0.04, 1, 1])

st.pyplot(fig, clear_figure=True)

if modify_rating:
    orig_val = base_ratings[base_skills.index(selected_skill)]
    st.info(
        f"**{selected_skill}** updated from **{orig_val:.1f}** to **{updated_rating:.1f}**. "
        f"The lowest-rated skill is **{lowest_skill}** ({lowest_val:.1f}); "
        "the chart title, visual emphasis, and takeaway updated automatically."
    )

with st.expander("View underlying summary table", expanded=False):
    st.dataframe(plot_df, use_container_width=True, hide_index=True)