import Mathlib

namespace CLUIOT

def Physical (x y z : ℝ) : Prop :=
  0 ≤ 1+x+y+z ∧ 0 ≤ 1+x-y-z ∧
  0 ≤ 1-x+y-z ∧ 0 ≤ 1-x-y+z

noncomputable def component (x y z : ℝ) : ℝ :=
  x * (5*y^2 + 5*z^2 - x^4 - 5*y^2*z^2) / 4

noncomputable def radial (a : ℝ) : ℝ := (5*a^3-3*a^5)/2

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

namespace CLUIOT

def bitForward (p : Bool × Bool) : Bool × Bool :=
  (Bool.xor p.1 p.2, p.1)

def bitBackward (p : Bool × Bool) : Bool × Bool :=
  (p.2, Bool.xor p.2 p.1)

theorem bit_left (p : Bool × Bool) : bitBackward (bitForward p) = p := by
  rcases p with ⟨a,b⟩
  cases a <;> cases b <;> rfl

theorem bit_right (p : Bool × Bool) : bitForward (bitBackward p) = p := by
  rcases p with ⟨a,b⟩
  cases a <;> cases b <;> rfl

theorem embed_left {α β : Type} (a : α) (b : β) :
    Prod.fst (a,b) = a := rfl

def butterfly (p : ℚ × ℚ) : ℚ × ℚ :=
  (p.1+p.2,p.1-p.2)

def unbutterfly (p : ℚ × ℚ) : ℚ × ℚ :=
  ((p.1+p.2)/2,(p.1-p.2)/2)

theorem butterfly_left (p : ℚ × ℚ) :
    unbutterfly (butterfly p) = p := by
  rcases p with ⟨a,b⟩
  apply Prod.ext <;> simp [butterfly, unbutterfly] <;> ring

theorem butterfly_right (p : ℚ × ℚ) :
    butterfly (unbutterfly p) = p := by
  rcases p with ⟨a,b⟩
  apply Prod.ext <;> simp [butterfly, unbutterfly] <;> ring

theorem conjugate_left {α β : Type} (W : α ≃ β) (T : α ≃ α) (x : β) :
    W (T.symm (W.symm (W (T (W.symm x))))) = x := by
  simp

theorem conjugate_right {α β : Type} (W : α ≃ β) (T : α ≃ α) (x : β) :
    W (T (W.symm (W (T.symm (W.symm x))))) = x := by
  simp

end CLUIOT

namespace CLUIOT

-- Abstract complete state: a bijective local update followed by a
-- head permutation selected by the updated data.
def stateForward {H D : Type} (U : H → D ≃ D)
    (M : D → H ≃ H) (s : H × D) : H × D :=
  let d := U s.1 s.2
  (M d s.1, d)

def stateBackward {H D : Type} (U : H → D ≃ D)
    (M : D → H ≃ H) (s : H × D) : H × D :=
  let h := (M s.2).symm s.1
  (h, (U h).symm s.2)

theorem state_left {H D : Type} (U : H → D ≃ D)
    (M : D → H ≃ H) (s : H × D) :
    stateBackward U M (stateForward U M s) = s := by
  rcases s with ⟨h,d⟩
  simp [stateForward, stateBackward]

theorem state_right {H D : Type} (U : H → D ≃ D)
    (M : D → H ≃ H) (s : H × D) :
    stateForward U M (stateBackward U M s) = s := by
  rcases s with ⟨h,d⟩
  simp [stateForward, stateBackward]

theorem compatible_extension {α β : Type} (T : α → α)
    (a : α) (b : β) :
    (fun p : α × β => (T p.1,p.2)) (a,b) = (T a,b) := rfl

end CLUIOT
