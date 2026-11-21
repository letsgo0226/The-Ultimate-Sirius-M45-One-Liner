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

namespace CLUIOT

theorem urfco_zero (l m : ℝ) :
    m^2 * (1+l^2) = 0 ↔ m = 0 := by
  constructor
  · intro h
    have hp : 0 < 1+l^2 := by nlinarith [sq_nonneg l]
    rcases mul_eq_zero.mp h with h0 | h0
    · nlinarith [sq_nonneg m]
    · linarith
  · intro h
    simp [h]

theorem urfco_center (l m : ℝ) :
    ((1/2 : ℝ)-1/2)^2 + m^2*(1+l^2) = 0 ↔ m = 0 := by
  simpa using urfco_zero l m

def urfcoBlock (l : ℚ) (v : ℚ × ℚ) : ℚ × ℚ :=
  (-v.1+l*v.2,v.2)

theorem urfco_block_involution (l : ℚ) (v : ℚ × ℚ) :
    urfcoBlock l (urfcoBlock l v) = v := by
  rcases v with ⟨a,b⟩
  apply Prod.ext <;> simp [urfcoBlock] <;> ring

theorem urfco_block_embed (l a : ℚ) :
    urfcoBlock l (a,0) = (-a,0) := by
  simp [urfcoBlock]

theorem urfco_projection {R : Type*} [Ring R]
    (t s x : R) (ht : t*t=1) (hs : s*s=1) :
    t*(x-t*x*s)+(x-t*x*s)*s=0 := by
  calc
    _ = t*x-(t*t)*x*s+x*s-t*x*(s*s) := by noncomm_ring
    _ = 0 := by rw [ht,hs]; noncomm_ring

theorem urfco_projection_complete {R : Type*} [Ring R]
    (t s a : R) (hs : s*s=1) (h : t*a+a*s=0) :
    a-t*a*s=a+a := by
  have h' := congrArg (fun z : R => z*s) h
  simp only [add_mul, zero_mul, mul_assoc, hs, mul_one] at h'
  have hh : t*(a*s) = -a := eq_neg_of_add_eq_zero_left h'
  rw [mul_assoc, hh]
  abel

end CLUIOT

namespace CLUIOT

-- Horner evaluation and its two-coefficient implementation model.
def uecsEval {R : Type*} [Ring R] (t : R) : List R → R
  | [] => 0
  | a :: cs => a + uecsEval t cs * t

def uecsReduce {R : Type*} [Ring R] : List R → R × R
  | [] => (0,0)
  | a :: cs => (a + (uecsReduce cs).2, (uecsReduce cs).1)

theorem uecs_horner_refinement {R : Type*} [Ring R]
    (t : R) (ht : t*t=1) (cs : List R) :
    uecsEval t cs = (uecsReduce cs).1 + (uecsReduce cs).2*t := by
  induction cs with
  | nil => simp [uecsEval, uecsReduce]
  | cons a cs ih =>
    simp only [uecsEval, uecsReduce]
    rw [ih]
    calc
      _ = a + (uecsReduce cs).1*t + (uecsReduce cs).2*(t*t) := by noncomm_ring
      _ = _ := by rw [ht]; noncomm_ring

theorem uecs_pair_mul {R : Type*} [CommRing R]
    (t a b c d : R) (ht : t*t=1) :
    (a+b*t)*(c+d*t) = (a*c+b*d)+(a*d+b*c)*t := by
  calc
    _ = a*c+(a*d+b*c)*t+b*d*(t*t) := by ring
    _ = _ := by rw [ht]; ring

end CLUIOT

namespace CLUIOT

theorem uecs_block_bound (a b l : ℝ) (hl : l^2 ≤ 1) :
    (-a+l*b)^2+b^2 ≤ 4*(a^2+b^2) := by
  have h : l^2*b^2 ≤ b^2 := by
    have h' := mul_nonneg (sub_nonneg.mpr hl) (sq_nonneg b)
    nlinarith only [h']
  nlinarith only [h, sq_nonneg (a+l*b), sq_nonneg a, sq_nonneg b]

theorem uecs_uniform_sum (xs ys : List ℝ)
    (h : List.Forall₂ (fun x y => y ≤ 4*x) xs ys) :
    ys.sum ≤ 4*xs.sum := by
  induction h with
  | nil => simp
  | cons hab habs ih =>
    simp only [List.sum_cons]
    linarith

theorem uecs_sequence_involution (l : ℕ → ℚ) (v : ℕ → ℚ × ℚ) :
    (fun k => urfcoBlock (l k) (urfcoBlock (l k) (v k))) = v := by
  funext k
  exact urfco_block_involution (l k) (v k)

end CLUIOT

namespace CLUIOT

def uecvEnergy : List ℝ → ℝ
  | [] => 0
  | r :: rs => r^2 + uecvEnergy rs

theorem uecv_energy_nonneg (rs : List ℝ) : 0 ≤ uecvEnergy rs := by
  induction rs with
  | nil => simp [uecvEnergy]
  | cons r rs ih =>
    exact add_nonneg (sq_nonneg r) ih

theorem uecv_energy_zero (rs : List ℝ) :
    uecvEnergy rs = 0 ↔ ∀ r ∈ rs, r = 0 := by
  induction rs with
  | nil => simp [uecvEnergy]
  | cons r rs ih =>
    constructor
    · intro h
      change r^2 + uecvEnergy rs = 0 at h
      have hn := uecv_energy_nonneg rs
      have hr : r = 0 := by nlinarith [sq_nonneg r]
      have ht : uecvEnergy rs = 0 := by nlinarith [sq_nonneg r]
      intro x hx
      rcases List.mem_cons.mp hx with he | hm
      · exact he.trans hr
      · exact ih.mp ht x hm
    · intro h
      have hr : r = 0 := h r (by simp)
      have ht : uecvEnergy rs = 0 :=
        ih.mpr (fun x hx => h x (List.mem_cons_of_mem r hx))
      simp [uecvEnergy, hr, ht]

noncomputable def uecvOmega (rs : List ℝ) (s : ℝ) : ℝ :=
  (s-1/2)^2 + uecvEnergy rs

theorem uecv_center_zero (rs : List ℝ) :
    uecvOmega rs (1/2) = 0 ↔ ∀ r ∈ rs, r = 0 := by
  simpa [uecvOmega] using uecv_energy_zero rs

theorem uecv_real_zero (rs : List ℝ) (s : ℝ) :
    uecvOmega rs s = 0 ↔ s = 1/2 ∧ ∀ r ∈ rs, r = 0 := by
  constructor
  · intro h
    change (s-1/2)^2 + uecvEnergy rs = 0 at h
    have hn := uecv_energy_nonneg rs
    have hs : s = 1/2 := by nlinarith [sq_nonneg (s-1/2)]
    have ht : uecvEnergy rs = 0 := by nlinarith [sq_nonneg (s-1/2)]
    exact ⟨hs, (uecv_energy_zero rs).mp ht⟩
  · rintro ⟨hs, hr⟩
    simp [uecvOmega, hs, (uecv_energy_zero rs).mpr hr]

end CLUIOT

namespace CLUIOT

theorem uecv_summable_blocks (a b l : ℕ → ℝ)
    (hl : ∀ k, (l k)^2 ≤ 1)
    (hv : Summable (fun k => (a k)^2 + (b k)^2)) :
    Summable (fun k => (-a k + l k*b k)^2 + (b k)^2) := by
  apply Summable.of_nonneg_of_le
    (f := fun k => (-a k + l k*b k)^2 + (b k)^2)
    (g := fun k => 4*((a k)^2 + (b k)^2))
  · intro k
    positivity
  · intro k
    exact uecs_block_bound (a k) (b k) (l k) (hl k)
  · exact hv.mul_left 4

theorem uecv_real_block_involution (a b l : ℝ) :
    -(-a+l*b)+l*b = a := by ring

theorem uecv_block_linear (a b c d l u v : ℝ) :
    -(u*a+v*c)+l*(u*b+v*d) =
      u*(-a+l*b)+v*(-c+l*d) := by ring

end CLUIOT
