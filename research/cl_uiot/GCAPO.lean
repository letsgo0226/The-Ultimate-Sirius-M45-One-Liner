import Mathlib

namespace CLUIOT

def Physical (x y z : ℝ) : Prop :=
  0 ≤ 1+x+y+z ∧ 0 ≤ 1+x-y-z ∧
  0 ≤ 1-x+y-z ∧ 0 ≤ 1-x-y+z

def component (x y z : ℝ) : ℝ :=
  x * (5*y^2 + 5*z^2 - x^4 - 5*y^2*z^2) / 4

def radial (a : ℝ) : ℝ := (5*a^3-3*a^5)/2

theorem diagonal (a : ℝ) : component a a a = radial a := by
  unfold component radial
  ring

theorem radial_factor (a : ℝ) :
    radial a - a = -a*(a^2-1)*(3*a^2-2)/2 := by
  unfold radial
  ring

theorem physical_sorted_constraint (x y z : ℝ)
    (h : Physical x y z) : x+y ≤ 1+z := by
  rcases h with ⟨_, _, _, h⟩
  linarith

theorem physical_x_bounds (x y z : ℝ)
    (h : Physical x y z) : -1 ≤ x ∧ x ≤ 1 := by
  rcases h with ⟨h1,h2,h3,h4⟩
  constructor <;> linarith

theorem complement_identity (b c : ℝ) :
    b+c-b*c = 1-(1-b)*(1-c) := by ring

theorem complement_mono (b B c C : ℝ)
    (hb : b ≤ B) (hc : c ≤ C) (hB : B ≤ 1) (hc1 : c ≤ 1) :
    b+c-b*c ≤ B+C-B*C := by
  have h1 := mul_nonneg (sub_nonneg.mpr hb) (sub_nonneg.mpr hc1)
  have h2 := mul_nonneg (sub_nonneg.mpr hc) (sub_nonneg.mpr hB)
  nlinarith

end CLUIOT
