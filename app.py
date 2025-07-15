import streamlit as st
import os
from dotenv import load_dotenv
from logic import ProductDiscoveryAnalyzer
from report_generator import ReportGenerator
import json
from typing import Dict, Optional

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Product Discovery Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'user_inputs' not in st.session_state:
    st.session_state.user_inputs = {}
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'follow_up_questions' not in st.session_state:
    st.session_state.follow_up_questions = []
if 'error' not in st.session_state:
    st.session_state.error = None
if 'case_study_enabled' not in st.session_state:
    st.session_state.case_study_enabled = False
if 'case_study_complete' not in st.session_state:
    st.session_state.case_study_complete = False

# Initialize analyzer and report generator
analyzer = ProductDiscoveryAnalyzer()
report_generator = ReportGenerator()

# Custom header with sticky positioning
st.markdown("""
    <div class="sticky-header">
        <h1>🎯 Product Discovery Assistant</h1>
        <p class="subtitle">Powered by AI-driven frameworks from top business schools</p>
    </div>
""", unsafe_allow_html=True)

# Description
st.markdown("""
    <div class="description">
        <p>Transform your product ideas into validated opportunities using proven frameworks from Stanford and Harvard. 
        Our AI-powered assistant guides you through Jobs to Be Done, Value Proposition Canvas, Opportunity Solution Tree, and the 4-Fit Model.</p>
    </div>
""", unsafe_allow_html=True)

# Main input section
with st.container():
    st.markdown("### 💡 Start Your Discovery")
    product_idea = st.text_area(
        "Describe your product idea or the customer problem you're trying to solve:",
        height=150,
        placeholder="Example: A mobile app that helps busy professionals find and book last-minute fitness classes...",
        help="Be specific about the problem you're solving or the product you're building. Include any relevant context about your target users."
    )

    # Case Study Mode toggle and company selection
    st.markdown("### 🧪 Case Study Mode")
    col1, col2 = st.columns([1, 2])
    with col1:
        case_study_enabled = st.toggle(
            "Enable Case Study Comparison",
            help="Compare your idea with successful companies to learn from their strategies"
        )
    with col2:
        if case_study_enabled:
            selected_company = st.selectbox(
                "Select a company to compare with:",
                options=analyzer.get_case_study_companies(),
                help="Choose a successful company to analyze similarities and differences"
            )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_button = st.button("Run Discovery", type="primary", use_container_width=True)

    if analyze_button:
        if not product_idea:
            st.error("Please enter a product idea or customer problem to analyze.")
        else:
            try:
                with st.spinner("🤔 Generating follow-up questions..."):
                    st.session_state.follow_up_questions = analyzer.get_follow_up_questions(product_idea)
                st.session_state.analysis_complete = False
                st.session_state.case_study_complete = False
                st.session_state.error = None
            except Exception as e:
                st.session_state.error = f"Error generating questions: {str(e)}"
                st.error(st.session_state.error)

# Follow-up questions section
if st.session_state.follow_up_questions:
    st.markdown("### 📝 Help Us Understand Better")
    st.markdown("Please answer these follow-up questions to improve our analysis:")
    
    for i, question in enumerate(st.session_state.follow_up_questions):
        if question.strip():  # Skip empty lines
            answer = st.text_area(
                f"Q{i+1}: {question}",
                key=f"q{i}",
                height=100
            )
            st.session_state.user_inputs[f"q{i}"] = answer

    col1, col2 = st.columns([1, 4])
    with col1:
        generate_button = st.button("Generate Analysis", type="primary", use_container_width=True)

    if generate_button:
        if product_idea:
            try:
                with st.spinner("🔍 Analyzing your product idea..."):
                    analysis_results = analyzer.analyze_all_frameworks(
                        product_idea,
                        st.session_state.user_inputs
                    )
                    st.session_state.analysis_complete = True
                    st.session_state.analysis_results = analysis_results
                    
                    # Generate case study if enabled
                    if case_study_enabled:
                        with st.spinner(f"📚 Analyzing comparison with {selected_company}..."):
                            case_study_results = analyzer.analyze_case_study(
                                product_idea,
                                selected_company,
                                st.session_state.user_inputs
                            )
                            st.session_state.case_study_results = case_study_results
                            st.session_state.case_study_complete = True
                    
                    st.session_state.error = None
            except Exception as e:
                st.session_state.error = f"Error during analysis: {str(e)}"
                st.error(st.session_state.error)

# Display analysis results
if st.session_state.analysis_complete:
    st.markdown("### 📊 Analysis Results")
    
    # JTBD Analysis
    with st.expander("🎯 Jobs to Be Done Analysis", expanded=True):
        st.markdown("""
            <div class="framework-header">
                <h3>Understanding what jobs your users are trying to get done</h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.analysis_results['jtbd']['analysis'])
        st.divider()
    
    # Value Proposition Analysis
    with st.expander("💎 Value Proposition Canvas", expanded=True):
        st.markdown("""
            <div class="framework-header">
                <h3>Mapping customer needs to your value proposition</h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.analysis_results['value_proposition']['analysis'])
        st.divider()
    
    # Opportunity Solution Tree Analysis
    with st.expander("🌳 Opportunity Solution Tree", expanded=True):
        st.markdown("""
            <div class="framework-header">
                <h3>Identifying opportunities and potential solutions</h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.analysis_results['opportunity_solution']['analysis'])
        st.divider()
    
    # 4-Fit Model Analysis
    with st.expander("🎯 4-Fit Model Assessment", expanded=True):
        st.markdown("""
            <div class="framework-header">
                <h3>Evaluating product-market fit and business model</h3>
            </div>
        """, unsafe_allow_html=True)
        st.markdown(st.session_state.analysis_results['four_fit']['analysis'])

    # Case Study Comparison
    if st.session_state.case_study_complete:
        st.markdown("### 🧪 Case Study Comparison")
        with st.expander(f"📚 Comparison with {st.session_state.case_study_results['company']}", expanded=True):
            st.markdown("""
                <div class="framework-header">
                    <h3>Learning from successful companies</h3>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.case_study_results['analysis'])

    # Download report section
    st.markdown("### 📥 Download Strategy Report")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📄 Download as Text", use_container_width=True):
            try:
                file_data, mime_type, file_extension = report_generator.generate_report(
                    product_idea,
                    st.session_state.analysis_results,
                    format='txt'
                )
                st.download_button(
                    label="📄 Download Text Report",
                    data=file_data,
                    file_name=f"product-discovery-report.{file_extension}",
                    mime=mime_type,
                    use_container_width=True
                )
                st.success("Text report generated successfully!")
            except Exception as e:
                st.error(f"Error generating text report: {str(e)}")
    
    with col2:
        if st.button("📑 Download as PDF", use_container_width=True):
            try:
                file_data, mime_type, file_extension = report_generator.generate_report(
                    product_idea,
                    st.session_state.analysis_results,
                    format='pdf'
                )
                st.download_button(
                    label="📑 Download PDF Report",
                    data=file_data,
                    file_name=f"product-discovery-report.{file_extension}",
                    mime=mime_type,
                    use_container_width=True
                )
                st.success("PDF report generated successfully!")
            except Exception as e:
                st.error(f"Error generating PDF report: {str(e)}")

# Footer
st.markdown("""
    <div class="footer">
        <p>Built with ❤️ using Streamlit and GPT-4 | 
        <a href="https://github.com/yourusername/product-discovery-assistant" target="_blank">View on GitHub</a></p>
    </div>
""", unsafe_allow_html=True) 