from typing import Tuple, Set, List


def precision_recall_f1(
        ground_truth: List[str], predicted: List[str]
) -> Tuple[float, float, float]:
    """
    Basic precision, recall, and F1-score for set membership:
      precision = TP / (TP + FP)
      recall    = TP / (TP + FN)
      f1        = 2 * precision * recall / (precision + recall)
    """
    gt_set = set(ground_truth)
    pred_set = set(predicted)

    tp = len(gt_set & pred_set)
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) else 0.0
    )
    return precision, recall, f1
