import argparse
import pandas as pd
from tqdm import tqdm
from src.config import STYLE_DESCRIPTIONS, DEFAULT_BASE_MODEL, DEFAULT_ADAPTER
from src.data import load_dataset, load_image
from src.prompt import build_user_content_2_pairs
from src.model import load_vision_model
from src.evaluate import run_inference, extract_multi_metrics

def main():
    parser = argparse.ArgumentParser(description="Evaluate a batch of images from a CSV.")
    parser.add_argument("--csv_path", type=str, required=True, help="Path to input CSV")
    parser.add_argument("--output_path", type=str, default="predictions_summary.csv", help="Path to save output CSV")
    parser.add_argument("--base_model", type=str, default=DEFAULT_BASE_MODEL)
    parser.add_argument("--adapter", type=str, default=DEFAULT_ADAPTER)
    parser.add_argument("--num_evals", type=int, default=0, help="Limit number of rows to evaluate (0 for all)")
    
    args = parser.parse_args()
    
    print(f"Loading dataset from {args.csv_path}...")
    df = load_dataset(args.csv_path, verify_paths=True)
    if args.num_evals > 0:
        df = df.head(args.num_evals)
    
    print(f"Found {len(df)} valid samples.")
    
    model, tokenizer = load_vision_model(args.base_model, args.adapter)
    
    predictions = []
    
    print("\nStarting batch inference...")
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        try:
            style = row.get("style", "unknown")
            style_desc = STYLE_DESCRIPTIONS.get(style, "distinctive textures, colors, and brushstrokes.")
            
            ex_a_src = load_image(row["ex_a_src_path"])
            ex_a_dst = load_image(row["ex_a_dst_path"])
            ex_b_src = load_image(row["ex_b_src_path"])
            ex_b_dst = load_image(row["ex_b_dst_path"])
            q_src = load_image(row["q_src_path"])
            q_res = load_image(row["q_res_path"])
            
            user_content = build_user_content_2_pairs(
                ex_a_src, ex_a_dst, ex_b_src, ex_b_dst, q_src, q_res, style_desc
            )
            
            raw_output, perf = run_inference(model, tokenizer, user_content, return_perf=True)
            metrics = extract_multi_metrics(raw_output)
            
            gt_value = row.get("final_score")
            gt_score = int(gt_value) if not pd.isna(gt_value) else None
            
            pred_record = {
                "sample_idx": idx,
                "row_id": row.get("row_id"),
                "style": style,
                "gt_final_score": gt_score,
                "pred_sf": metrics["sf"],
                "pred_cp": metrics["cp"],
                "pred_rq": metrics["rq"],
                "pred_final_score": metrics["final_scaled_score"],
                "parse_failed": not metrics["parsed"],
                "ttft_sec": perf["ttft_sec"],
                "tpot_sec": perf["tpot_sec"],
                "prefill_time_sec": perf["prefill_time_sec"],
                "total_time_sec": perf["total_time_sec"],
                "peak_vram_gb": perf["peak_vram_gb"],
                "avg_gpu_utilization_pct": perf["avg_gpu_utilization_pct"],
                "avg_power_consumption_w": perf["avg_power_consumption_w"],
                "hardware_info": str(perf["hardware_info"]),
                "raw_model_output": raw_output
            }
            predictions.append(pred_record)
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            
    out_df = pd.DataFrame(predictions)
    out_df.to_csv(args.output_path, index=False)
    print(f"\nSaved {len(out_df)} predictions to {args.output_path}")

    if not out_df.empty:
        scored = out_df.loc[~out_df["parse_failed"]].dropna(subset=["gt_final_score", "pred_final_score"])
        if not scored.empty:
            errors = (scored["pred_final_score"] - scored["gt_final_score"]).abs()
            print(f"Accuracy (parsed rows): {(errors == 0).mean():.1%}")
            print(f"Within ±1 (parsed rows): {(errors <= 1).mean():.1%}")
            print(f"MAE (parsed rows): {errors.mean():.3f}")

    parse_failures = int(out_df["parse_failed"].sum()) if not out_df.empty else 0
    print(f"Parse failures: {parse_failures}")

if __name__ == "__main__":
    main()
