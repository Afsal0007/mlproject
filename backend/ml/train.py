"""
Placement AI — ML Training Script (Phase 0 stub)
Full implementation in Phase 3.

Usage:
    python ml/train.py --data ../data/raw/placement_dataset.csv \
                       --output ml/models/ \
                       --version v1
"""
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Placement AI models")
    parser.add_argument("--data", required=True, help="Path to raw CSV dataset")
    parser.add_argument("--output", required=True, help="Directory to save model artifacts")
    parser.add_argument("--version", default="v1", help="Model version tag")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"[Phase 0 stub] Training not yet implemented.")
    print(f"  data={args.data}, output={args.output}, version={args.version}, seed={args.seed}")


if __name__ == "__main__":
    main()
