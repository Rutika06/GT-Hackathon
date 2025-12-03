from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os

from app.ingest.csv_load import load_csv
from app.processing.transform import standardize_dates
from app.processing.kpcalc import numeric_summary, category_summary, time_series_summary
from app.text_gen.prompt import build_summary_for_llm, build_llm_prompt
from app.text_gen.llmcl import generate_insights
from app.report_gen.ppt import generate_ppt_report
from app.report_gen.pdf import generate_pdf_report  # NEW
from app.utils.log import logger

app = FastAPI(title="Automated Insight Engine")


@app.get("/")
def health():
    return {"status": "ok", "message": "Insight Engine Ready 🚀"}


@app.post("/generate-report")
async def generate_report(data_csv: UploadFile = File(...)):
    try:
        logger.info("Reading uploaded CSV...")
        file_bytes = await data_csv.read()
        df = load_csv(file_bytes)

        logger.info("Cleaning & analyzing dataset...")
        df = standardize_dates(df)

        num_sum = numeric_summary(df)
        cat_sum = category_summary(df)
        ts_sum = time_series_summary(df)

        logger.info("Building LLM prompt...")
        summary_text = build_summary_for_llm(df, num_sum, cat_sum, ts_sum)
        prompt = build_llm_prompt(summary_text)

        logger.info("Generating executive insights from LLM...")
        insights_text = generate_insights(prompt)

        os.makedirs("report", exist_ok=True)

        ppt_path = os.path.join("report", "Dataset_Insight_Report.pptx")
        pdf_path = os.path.join("report", "Dataset_Insight_Report.pdf")

        logger.info("Creating PPTX report...")
        generate_ppt_report(
            dataset_name=data_csv.filename,
            df=df,
            insights_text=insights_text,
            output_path=ppt_path,
        )

        logger.info("Creating PDF report...")
        generate_pdf_report(
            dataset_name=data_csv.filename,
            df=df,
            insights_text=insights_text,
            output_path=pdf_path,
        )

        logger.info("Report files generated successfully 🚀")

        return JSONResponse(
            {
                "message": "Report generated successfully 🎉",
                "ppt_path": "/download?file=Dataset_Insight_Report.pptx",
                "pdf_path": "/download?file=Dataset_Insight_Report.pdf",
            }
        )

    except Exception as e:
        logger.exception("Error while generating report")
        raise HTTPException(status_code=500, detail=str(e))


# File Download Endpoint
@app.get("/download")
def download_report(file: str):
    file_path = os.path.join("report", file)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, filename=file)
