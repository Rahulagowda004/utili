import streamlit as st
import pandas as pd
import os
from pathlib import Path
from utils import pipeline
import tempfile

def main():
    st.set_page_config(
        page_title="Utilization Report Generator",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Utilization Report Generator")
    st.markdown("Upload a CSV file to process it through the pipeline and download the results.")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload a CSV file to process through the pipeline"
    )
    
    if uploaded_file is not None:
        try:
            # Display file info
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size} bytes"
            }
            st.json(file_details)
            
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Display preview of the data
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), width='stretch')
            
            # Show basic statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", len(df))
            with col2:
                st.metric("Total Columns", len(df.columns))
            with col3:
                st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
            
            # Process button
            if st.button("🚀 Process Data", type="primary", width='stretch'):
                with st.spinner("Processing data through pipeline..."):
                    try:
                        # Save uploaded file temporarily to artifacts folder
                        artifacts_dir = Path("artifacts")
                        artifacts_dir.mkdir(exist_ok=True)
                        
                        temp_input_path = artifacts_dir / "temp_input.csv"
                        df.to_csv(temp_input_path, index=False)
                        
                        # Process through pipeline
                        result_path = pipeline(df)
                        
                        # Check if result file exists
                        if result_path and Path(result_path).exists():
                            st.success("✅ Processing completed successfully!")
                            
                            # Display download section
                            st.subheader("📥 Download Results")
                            
                            # Read the result file for download
                            with open(result_path, "rb") as file:
                                file_data = file.read()
                            
                            # Get file extension for proper mime type
                            file_ext = Path(result_path).suffix.lower()
                            if file_ext == '.xlsx':
                                mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                file_name = f"processed_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                            elif file_ext == '.csv':
                                mime_type = 'text/csv'
                                file_name = f"processed_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
                            else:
                                mime_type = 'application/octet-stream'
                                file_name = f"processed_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
                            
                            # Download button
                            st.download_button(
                                label="📁 Download Processed File",
                                data=file_data,
                                file_name=file_name,
                                mime=mime_type,
                                width='stretch'
                            )
                            
                            # Show file info
                            file_size = len(file_data)
                            st.info(f"📄 File ready for download: {file_name} ({file_size:,} bytes)")
                            
                            # Clean up temporary file
                            if temp_input_path.exists():
                                temp_input_path.unlink()
                                
                        else:
                            st.error("❌ Processing failed. No output file was generated.")
                            
                    except Exception as e:
                        st.error(f"❌ Error during processing: {str(e)}")
                        # Clean up temporary file in case of error
                        if 'temp_input_path' in locals() and temp_input_path.exists():
                            temp_input_path.unlink()
            
            # Optional: Show column information
            with st.expander("📊 Column Information"):
                # Fix the Arrow serialization issue by converting dtypes to strings
                col_info = pd.DataFrame({
                    'Column': df.columns.tolist(),
                    'Data Type': [str(dtype) for dtype in df.dtypes],
                    'Non-Null Count': df.count().tolist(),
                    'Null Count': df.isnull().sum().tolist()
                })
                st.dataframe(col_info, width='stretch')
                
        except Exception as e:
            st.error(f"❌ Error reading CSV file: {str(e)}")
            st.info("Please make sure your file is a valid CSV format.")
    
    else:
        st.info("👆 Please upload a CSV file to get started.")
        
        # Show example of expected format
        with st.expander("💡 Example CSV Format"):
            example_data = {
                'Column1': ['Value1', 'Value2', 'Value3'],
                'Column2': [100, 200, 300],
                'Column3': ['A', 'B', 'C']
            }
            example_df = pd.DataFrame(example_data)
            st.dataframe(example_df, width='stretch')

if __name__ == "__main__":
    main()