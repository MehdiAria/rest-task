from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import cv2
import numpy as np


@dataclass
class DetectionResult:
    found: bool
    confidence: float
    location: tuple[int, int] | None = None


def locate_element(screen: np.ndarray, templates: Iterable[Path], threshold: float = 0.86) -> DetectionResult:
    best = DetectionResult(found=False, confidence=0.0)
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    for template_path in templates:
        tpl = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
        if tpl is None:
            continue
        result = cv2.matchTemplate(gray_screen, tpl, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > best.confidence:
            best = DetectionResult(found=max_val >= threshold, confidence=float(max_val), location=max_loc)
    return best
