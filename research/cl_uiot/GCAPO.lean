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
    (g := fun k => (-a k + l k*b k)^2 + (b k)^2)
    (f := fun k => 4*((a k)^2 + (b k)^2))
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

namespace CLUIOT

def ufrsStep (n : ℕ) (b : Fin 256) : ℕ :=
  257*n + b.val + 1

theorem ufrs_step_div (n : ℕ) (b : Fin 256) :
    ufrsStep n b / 257 = n := by
  have hb := b.isLt
  unfold ufrsStep
  omega

theorem ufrs_step_mod (n : ℕ) (b : Fin 256) :
    ufrsStep n b % 257 = b.val + 1 := by
  have hb := b.isLt
  unfold ufrsStep
  omega

theorem ufrs_step_injective (n m : ℕ) (a b : Fin 256)
    (h : ufrsStep n a = ufrsStep m b) : n = m ∧ a = b := by
  constructor
  · have hd := congrArg (fun x : ℕ => x / 257) h
    simpa only [ufrs_step_div] using hd
  · apply Fin.ext
    have hm := congrArg (fun x : ℕ => x % 257) h
    simp only [ufrs_step_mod] at hm
    omega

end CLUIOT

namespace CLUIOT

-- Least significant byte first; reverse the input for the Python order.
def ufrsEncode : List (Fin 256) → ℕ
  | [] => 1
  | b :: bs => ufrsStep (ufrsEncode bs) b

def ufrsDecode : ℕ → ℕ → Option (List (Fin 256))
  | 0, n => if n = 1 then some [] else none
  | fuel + 1, n =>
    if n = 1 then some [] else
      let r := n % 257
      if h : 0 < r ∧ r ≤ 256 then
        (ufrsDecode fuel (n / 257)).map
          (fun bs => ⟨r-1, by omega⟩ :: bs)
      else none

theorem ufrs_encode_positive (bs : List (Fin 256)) :
    0 < ufrsEncode bs := by
  cases bs with
  | nil => simp [ufrsEncode]
  | cons b bs => simp only [ufrsEncode, ufrsStep]; omega

theorem ufrs_decode_encode (bs : List (Fin 256)) :
    ufrsDecode bs.length (ufrsEncode bs) = some bs := by
  induction bs with
  | nil => simp [ufrsEncode, ufrsDecode]
  | cons b bs ih =>
    have hp := ufrs_encode_positive bs
    have hn : ufrsStep (ufrsEncode bs) b ≠ 1 := by
      unfold ufrsStep
      omega
    have hb : 0 < b.val + 1 ∧ b.val + 1 ≤ 256 := by
      have hh := b.isLt
      omega
    simp only [List.length_cons, ufrsEncode, ufrsDecode, hn, if_false,
      ufrs_step_mod, ufrs_step_div, hb, dite_true, ih, Option.map_some]
    congr

theorem ufrs_encode_injective_same_length (a b : List (Fin 256))
    (hl : a.length = b.length) (he : ufrsEncode a = ufrsEncode b) :
    a = b := by
  have h := ufrs_decode_encode a
  rw [hl, he, ufrs_decode_encode] at h
  exact Option.some.inj h.symm

end CLUIOT

namespace CLUIOT

theorem ufrs_encode_injective (a b : List (Fin 256))
    (h : ufrsEncode a = ufrsEncode b) : a = b := by
  induction a generalizing b with
  | nil =>
    cases b with
    | nil => rfl
    | cons y ys =>
      have hp := ufrs_encode_positive ys
      simp only [ufrsEncode, ufrsStep] at h
      omega
  | cons x xs ih =>
    cases b with
    | nil =>
      have hp := ufrs_encode_positive xs
      simp only [ufrsEncode, ufrsStep] at h
      omega
    | cons y ys =>
      change ufrsStep (ufrsEncode xs) x = ufrsStep (ufrsEncode ys) y at h
      obtain ⟨ht, hh⟩ := ufrs_step_injective _ _ _ _ h
      rw [hh, ih ys ht]

inductive UfrsOp where
  | add | sub | mul | div

def ufrsExact (op : UfrsOp) (a b : ℚ) : ℚ :=
  match op with
  | .add => a+b
  | .sub => a-b
  | .mul => a*b
  | .div => a/b

def ufrsGuard (op : UfrsOp) (a b : ℚ) (cost budget : ℕ) : Option ℚ :=
  if cost ≤ budget then
    match op with
    | .div => if b = 0 then none else some (ufrsExact op a b)
    | _ => some (ufrsExact op a b)
  else none

theorem ufrs_guard_sound (op : UfrsOp) (a b v : ℚ) (cost budget : ℕ)
    (h : ufrsGuard op a b cost budget = some v) :
    v = ufrsExact op a b := by
  by_cases hc : cost ≤ budget
  · cases op <;> simp [ufrsGuard, hc] at h
    · exact h.symm
    · exact h.symm
    · exact h.symm
    · by_cases hz : b = 0 <;> simp_all
  · simp [ufrsGuard, hc] at h

theorem ufrs_guard_over_budget (op : UfrsOp) (a b : ℚ) (cost budget : ℕ)
    (h : budget < cost) : ufrsGuard op a b cost budget = none := by
  simp [ufrsGuard, Nat.not_le.mpr h]

theorem ufrs_guard_div_zero (a : ℚ) (cost budget : ℕ) :
    ufrsGuard .div a 0 cost budget = none := by
  by_cases h : cost ≤ budget <;> simp [ufrsGuard, h]

end CLUIOT

namespace CLUIOT

inductive UfrsExpr where
  | var
  | lit (q : ℚ)
  | add (a b : UfrsExpr)
  | sub (a b : UfrsExpr)
  | mul (a b : UfrsExpr)

def ufrsEval (x : ℚ) : UfrsExpr → ℚ
  | .var => x
  | .lit q => q
  | .add a b => ufrsEval x a + ufrsEval x b
  | .sub a b => ufrsEval x a - ufrsEval x b
  | .mul a b => ufrsEval x a * ufrsEval x b

noncomputable def ufrsNormalize : UfrsExpr → Polynomial ℚ
  | .var => Polynomial.X
  | .lit q => Polynomial.C q
  | .add a b => ufrsNormalize a + ufrsNormalize b
  | .sub a b => ufrsNormalize a - ufrsNormalize b
  | .mul a b => ufrsNormalize a * ufrsNormalize b

theorem ufrs_normalize_sound (e : UfrsExpr) (x : ℚ) :
    (ufrsNormalize e).eval x = ufrsEval x e := by
  induction e with
  | var => simp [ufrsNormalize, ufrsEval]
  | lit q => simp [ufrsNormalize, ufrsEval]
  | add a b ha hb => simp [ufrsNormalize, ufrsEval, ha, hb]
  | sub a b ha hb => simp [ufrsNormalize, ufrsEval, ha, hb]
  | mul a b ha hb => simp [ufrsNormalize, ufrsEval, ha, hb]

theorem ufrs_normalize_identity (a b : UfrsExpr)
    (h : ufrsNormalize a = ufrsNormalize b) (x : ℚ) :
    ufrsEval x a = ufrsEval x b := by
  rw [← ufrs_normalize_sound a x, ← ufrs_normalize_sound b x, h]

theorem ufrs_normalize_counterexample (a b : UfrsExpr) (x : ℚ)
    (h : ufrsEval x a ≠ ufrsEval x b) :
    ufrsNormalize a ≠ ufrsNormalize b := by
  intro he
  exact h (ufrs_normalize_identity a b he x)

end CLUIOT

namespace CLUIOT

-- Root-count bound is explicit in this first certificate model.
theorem ufrs_finite_root_certificate (p : Polynomial ℚ) (s : Finset ℚ)
    (d : ℕ) (hcount : p ≠ 0 → s.card ≤ p.natDegree)
    (hdeg : p.natDegree ≤ d) (hsize : d < s.card) : p = 0 := by
  by_contra hn
  have hc := hcount hn
  omega

theorem ufrs_residual_certificate (a b : UfrsExpr) (s : Finset ℚ)
    (d : ℕ)
    (hcount : ufrsNormalize a - ufrsNormalize b ≠ 0 →
      s.card ≤ (ufrsNormalize a - ufrsNormalize b).natDegree)
    (hdeg : (ufrsNormalize a - ufrsNormalize b).natDegree ≤ d)
    (hsize : d < s.card) (x : ℚ) :
    ufrsEval x a = ufrsEval x b := by
  have hz := ufrs_finite_root_certificate
    (ufrsNormalize a - ufrsNormalize b) s d hcount hdeg hsize
  exact ufrs_normalize_identity a b (sub_eq_zero.mp hz) x

theorem ufrs_dual_consistent (a b : UfrsExpr)
    (h : ufrsNormalize a = ufrsNormalize b) :
    ¬ ∃ x : ℚ, ufrsEval x a ≠ ufrsEval x b := by
  rintro ⟨x, hx⟩
  exact hx (ufrs_normalize_identity a b h x)

end CLUIOT

namespace CLUIOT

def UfrsSquareSummable (v : ℕ → ℝ × ℝ) : Prop :=
  Summable (fun k => (v k).1^2 + (v k).2^2)

noncomputable def ufrsCoupling (k : ℕ) : ℝ := 1 / ((k : ℝ)+1)

theorem ufrs_coupling_bound (k : ℕ) : (ufrsCoupling k)^2 ≤ 1 := by
  have h : (1 : ℝ) ≤ (k : ℝ)+1 := by
    have hk : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
    linarith
  have hp : (0 : ℝ) < (k : ℝ)+1 := by positivity
  have h1 : ufrsCoupling k ≤ 1 := by
    unfold ufrsCoupling
    exact (div_le_iff₀ hp).2 (by linarith)
  have h0 : 0 ≤ ufrsCoupling k := by unfold ufrsCoupling; positivity
  nlinarith [mul_nonneg h0 (sub_nonneg.mpr h1)]

noncomputable def ufrsTransform (v : ℕ → ℝ × ℝ) : ℕ → ℝ × ℝ :=
  fun k => (-(v k).1 + ufrsCoupling k * (v k).2, (v k).2)

theorem ufrs_transform_closed (v : ℕ → ℝ × ℝ)
    (h : UfrsSquareSummable v) : UfrsSquareSummable (ufrsTransform v) := by
  exact uecv_summable_blocks (fun k => (v k).1) (fun k => (v k).2)
    ufrsCoupling ufrs_coupling_bound h

theorem ufrs_transform_involution (v : ℕ → ℝ × ℝ) :
    ufrsTransform (ufrsTransform v) = v := by
  funext k
  apply Prod.ext
  · change -(-(v k).1 + ufrsCoupling k * (v k).2) +
        ufrsCoupling k * (v k).2 = (v k).1
    ring
  · rfl

end CLUIOT

namespace CLUIOT

inductive UfrsVerdict where
  | proof
  | counterexample (x : ℚ)
  | unknown

noncomputable def ufrsCheck (a b : UfrsExpr) (v : UfrsVerdict) : Prop :=
  match v with
  | .proof => ufrsNormalize a = ufrsNormalize b
  | .counterexample x => ufrsEval x a ≠ ufrsEval x b
  | .unknown => False

def ufrsSpecification (a b : UfrsExpr) (v : UfrsVerdict) : Prop :=
  match v with
  | .proof => ∀ x : ℚ, ufrsEval x a = ufrsEval x b
  | .counterexample x => ufrsEval x a ≠ ufrsEval x b
  | .unknown => False

theorem ufrs_check_sound (a b : UfrsExpr) (v : UfrsVerdict)
    (h : ufrsCheck a b v) : ufrsSpecification a b v := by
  cases v with
  | proof =>
    intro x
    exact ufrs_normalize_identity a b h x
  | counterexample x => exact h
  | unknown => exact h

theorem ufrs_check_conflict (a b : UfrsExpr) (x : ℚ)
    (hp : ufrsCheck a b .proof)
    (hc : ufrsCheck a b (.counterexample x)) : False := by
  exact hc (ufrs_normalize_identity a b hp x)

theorem ufrs_check_unknown (a b : UfrsExpr) :
    ¬ ufrsCheck a b .unknown := by
  simp [ufrsCheck]

end CLUIOT

namespace CLUIOT

def efrcEncode (bs : List (Fin 256)) : ℕ :=
  bs.foldl ufrsStep 1

theorem efrc_fold_reverse (bs : List (Fin 256)) (acc : List (Fin 256)) :
    bs.foldl ufrsStep (ufrsEncode acc) = ufrsEncode (bs.reverse ++ acc) := by
  induction bs generalizing acc with
  | nil => simp
  | cons b bs ih =>
    change bs.foldl ufrsStep (ufrsEncode (b :: acc)) =
      ufrsEncode ((b :: bs).reverse ++ acc)
    rw [ih]
    simp [List.reverse_cons, List.append_assoc]

theorem efrc_encode_order (bs : List (Fin 256)) :
    efrcEncode bs = ufrsEncode bs.reverse := by
  simpa [efrcEncode, ufrsEncode] using efrc_fold_reverse bs []

theorem efrc_decode_extra_fuel (bs : List (Fin 256)) (extra : ℕ) :
    ufrsDecode (bs.length + extra) (ufrsEncode bs) = some bs := by
  induction bs with
  | nil =>
    cases extra <;> simp [ufrsEncode, ufrsDecode]
  | cons b bs ih =>
    have hp := ufrs_encode_positive bs
    have hn : ufrsStep (ufrsEncode bs) b ≠ 1 := by
      unfold ufrsStep
      omega
    have hb : 0 < b.val + 1 ∧ b.val + 1 ≤ 256 := by
      have hh := b.isLt
      omega
    rw [List.length_cons, Nat.succ_add]
    simp only [ufrsEncode, ufrsDecode, hn, if_false, ufrs_step_mod,
      ufrs_step_div, hb, dite_true, ih, Option.map_some]
    congr

theorem efrc_bounded_roundtrip (bs : List (Fin 256)) (fuel : ℕ)
    (h : bs.length ≤ fuel) :
    (ufrsDecode fuel (efrcEncode bs)).map List.reverse = some bs := by
  have he : fuel = bs.reverse.length + (fuel - bs.reverse.length) := by
    simp only [List.length_reverse]
    omega
  rw [efrc_encode_order, he, efrc_decode_extra_fuel]
  simp

end CLUIOT

namespace CLUIOT

theorem efrc_decode_sound (fuel n : ℕ) (bs : List (Fin 256))
    (h : ufrsDecode fuel n = some bs) :
    ufrsEncode bs = n ∧ bs.length ≤ fuel := by
  induction fuel generalizing n bs with
  | zero =>
    by_cases hn : n = 1
    · subst n
      simp [ufrsDecode] at h
      subst bs
      simp [ufrsEncode]
    · simp [ufrsDecode, hn] at h
  | succ fuel ih =>
    by_cases hn : n = 1
    · subst n
      simp [ufrsDecode] at h
      subst bs
      simp [ufrsEncode]
    · by_cases hr : 0 < n % 257 ∧ n % 257 ≤ 256
      · simp only [ufrsDecode, hn, if_false, hr, dite_true] at h
        cases hd : ufrsDecode fuel (n / 257) with
        | none => simp [hd] at h
        | some tail =>
          simp [hd] at h
          subst bs
          obtain ⟨he, hl⟩ := ih _ _ hd
          constructor
          · simp only [ufrsEncode, ufrsStep, he]
            have hm := Nat.mod_add_div n 257
            omega
          · simp only [List.length_cons]
            omega
      · simp [ufrsDecode, hn, hr] at h

theorem efrc_decode_iff (fuel n : ℕ) (bs : List (Fin 256)) :
    ufrsDecode fuel n = some bs ↔
      ufrsEncode bs = n ∧ bs.length ≤ fuel := by
  constructor
  · exact efrc_decode_sound fuel n bs
  · rintro ⟨he, hl⟩
    rw [← he]
    have hf : fuel = bs.length + (fuel - bs.length) := by omega
    rw [hf]
    exact efrc_decode_extra_fuel bs _

theorem efrc_decode_reject (fuel n : ℕ) :
    ufrsDecode fuel n = none ↔
      ¬ ∃ bs : List (Fin 256), ufrsEncode bs = n ∧ bs.length ≤ fuel := by
  constructor
  · intro h hex
    obtain ⟨bs, hb⟩ := hex
    have hs := (efrc_decode_iff fuel n bs).mpr hb
    rw [h] at hs
    cases hs
  · intro h
    cases hd : ufrsDecode fuel n with
    | none => rfl
    | some bs => exact False.elim (h ⟨bs, efrc_decode_sound fuel n bs hd⟩)

end CLUIOT

namespace CLUIOT

def EfrcFits (a : ℕ) (k : ℕ) : Prop := a < 2^k

theorem efrc_fits_mul (a b k l : ℕ)
    (ha : EfrcFits a k) (hb : EfrcFits b l) :
    EfrcFits (a*b) (k+l) := by
  unfold EfrcFits at *
  rw [pow_add]
  have hp : 0 < (2 : ℕ)^k := by positivity
  calc
    a*b ≤ (2^k)*b := Nat.mul_le_mul_right b (Nat.le_of_lt ha)
    _ < (2^k)*(2^l) := Nat.mul_lt_mul_of_pos_left hb hp

theorem efrc_fits_add (a b k : ℕ)
    (ha : EfrcFits a k) (hb : EfrcFits b k) :
    EfrcFits (a+b) (k+1) := by
  unfold EfrcFits at *
  rw [pow_succ]
  omega

theorem efrc_fits_mono (a k l : ℕ)
    (ha : EfrcFits a k) (hkl : k ≤ l) : EfrcFits a l := by
  obtain ⟨d, hd⟩ := Nat.exists_eq_add_of_le hkl
  subst l
  unfold EfrcFits at *
  rw [pow_add]
  have hp : 0 < (2 : ℕ)^d := by positivity
  exact lt_of_lt_of_le ha (by
    calc
      (2 : ℕ)^k = 2^k * 1 := by simp
      _ ≤ 2^k * 2^d := Nat.mul_le_mul_left _ (by omega))

theorem efrc_cross_sum_bound (a b c d n m k l : ℕ)
    (ha : EfrcFits a n) (hb : EfrcFits b m)
    (hc : EfrcFits c k) (hd : EfrcFits d l) :
    EfrcFits (a*d+b*c) (max (n+l) (m+k)+1) := by
  apply efrc_fits_add
  · exact efrc_fits_mono _ _ _ (efrc_fits_mul _ _ _ _ ha hd) (le_max_left _ _)
  · exact efrc_fits_mono _ _ _ (efrc_fits_mul _ _ _ _ hb hc) (le_max_right _ _)

end CLUIOT

namespace CLUIOT

theorem efrc_signed_mul (a b : ℤ) (k l : ℕ)
    (ha : EfrcFits a.natAbs k) (hb : EfrcFits b.natAbs l) :
    EfrcFits (a*b).natAbs (k+l) := by
  rw [Int.natAbs_mul]
  exact efrc_fits_mul _ _ _ _ ha hb

theorem efrc_signed_add (a b : ℤ) (k : ℕ)
    (ha : EfrcFits a.natAbs k) (hb : EfrcFits b.natAbs k) :
    EfrcFits (a+b).natAbs (k+1) := by
  have h := efrc_fits_add _ _ _ ha hb
  exact lt_of_le_of_lt (Int.natAbs_add_le a b) h

theorem efrc_signed_cross (a b c d : ℤ) (n m k l : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l) :
    EfrcFits (a*d+b*c).natAbs (max (n+l) (m+k)+1) := by
  apply efrc_signed_add
  · exact efrc_fits_mono _ _ _ (efrc_signed_mul a d n l ha hd) (le_max_left _ _)
  · exact efrc_fits_mono _ _ _ (efrc_signed_mul b c m k hb hc) (le_max_right _ _)

theorem efrc_reduction_bound (a g k : ℕ)
    (ha : EfrcFits a k) :
    EfrcFits (a/g) k := by
  exact lt_of_le_of_lt (Nat.div_le_self a g) ha

end CLUIOT

namespace CLUIOT

theorem efrc_signed_sub (a b : ℤ) (k : ℕ)
    (ha : EfrcFits a.natAbs k) (hb : EfrcFits b.natAbs k) :
    EfrcFits (a-b).natAbs (k+1) := by
  rw [sub_eq_add_neg]
  apply efrc_signed_add a (-b) k ha
  simpa using hb

theorem efrc_add_budget (a b c d : ℤ) (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : max (max (n+l) (m+k)+1) (m+l) ≤ B) :
    EfrcFits (a*d+b*c).natAbs B ∧ EfrcFits (b*d).natAbs B := by
  constructor
  · exact efrc_fits_mono _ _ _ (efrc_signed_cross a b c d n m k l ha hb hc hd)
      (le_trans (le_max_left _ _) hB)
  · exact efrc_fits_mono _ _ _ (efrc_signed_mul b d m l hb hd)
      (le_trans (le_max_right _ _) hB)

theorem efrc_mul_budget (a b c d : ℤ) (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : max (n+k) (m+l) ≤ B) :
    EfrcFits (a*c).natAbs B ∧ EfrcFits (b*d).natAbs B := by
  exact ⟨efrc_fits_mono _ _ _ (efrc_signed_mul a c n k ha hc)
    (le_trans (le_max_left _ _) hB),
    efrc_fits_mono _ _ _ (efrc_signed_mul b d m l hb hd)
    (le_trans (le_max_right _ _) hB)⟩

theorem efrc_div_budget (a b c d : ℤ) (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : max (n+l) (m+k) ≤ B) :
    EfrcFits (a*d).natAbs B ∧ EfrcFits (b*c).natAbs B := by
  exact efrc_mul_budget a b d c n m l k B ha hb hd hc hB

end CLUIOT

namespace CLUIOT

theorem efrc_sub_budget (a b c d : ℤ) (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : max (max (n+l) (m+k)+1) (m+l) ≤ B) :
    EfrcFits (a*d-b*c).natAbs B ∧ EfrcFits (b*d).natAbs B := by
  have h := efrc_add_budget a b (-c) d n m k l B ha hb
    (by simpa using hc) hd hB
  simpa [mul_neg, sub_eq_add_neg] using h

theorem efrc_reduce_pair (a b g B : ℕ)
    (ha : EfrcFits a B) (hb : EfrcFits b B) :
    EfrcFits (a/g) B ∧ EfrcFits (b/g) B :=
  ⟨efrc_reduction_bound a g B ha, efrc_reduction_bound b g B hb⟩

theorem efrc_gcd_budget (a b B : ℕ)
    (ha : EfrcFits a B) (hb : EfrcFits b B) :
    EfrcFits (a / Nat.gcd a b) B ∧
    EfrcFits (b / Nat.gcd a b) B :=
  efrc_reduce_pair a b (Nat.gcd a b) B ha hb

theorem efrc_add_reduced_budget (a b c d : ℤ) (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : max (max (n+l) (m+k)+1) (m+l) ≤ B) :
    let u := (a*d+b*c).natAbs
    let v := (b*d).natAbs
    EfrcFits (u / Nat.gcd u v) B ∧ EfrcFits (v / Nat.gcd u v) B := by
  obtain ⟨hu, hv⟩ := efrc_add_budget a b c d n m k l B ha hb hc hd hB
  exact efrc_gcd_budget _ _ B hu hv

end CLUIOT

namespace CLUIOT

def efrcRaw (op : UfrsOp) (a b c d : ℤ) : ℤ × ℤ :=
  match op with
  | .add => (a*d+b*c,b*d)
  | .sub => (a*d-b*c,b*d)
  | .mul => (a*c,b*d)
  | .div => (a*d,b*c)

def efrcCost (op : UfrsOp) (n m k l : ℕ) : ℕ :=
  match op with
  | .add | .sub => max (max (n+l) (m+k)+1) (m+l)
  | .mul => max (n+k) (m+l)
  | .div => max (n+l) (m+k)

theorem efrc_raw_budget (op : UfrsOp) (a b c d : ℤ) (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : efrcCost op n m k l ≤ B) :
    EfrcFits (efrcRaw op a b c d).1.natAbs B ∧
    EfrcFits (efrcRaw op a b c d).2.natAbs B := by
  cases op
  · exact efrc_add_budget a b c d n m k l B ha hb hc hd hB
  · exact efrc_sub_budget a b c d n m k l B ha hb hc hd hB
  · exact efrc_mul_budget a b c d n m k l B ha hb hc hd hB
  · exact efrc_div_budget a b c d n m k l B ha hb hc hd hB

theorem efrc_raw_den_nonzero (op : UfrsOp) (a b c d : ℤ)
    (hb : b ≠ 0) (hd : d ≠ 0)
    (hc : op = .div → c ≠ 0) :
    (efrcRaw op a b c d).2 ≠ 0 := by
  cases op
  · exact mul_ne_zero hb hd
  · exact mul_ne_zero hb hd
  · exact mul_ne_zero hb hd
  · exact mul_ne_zero hb (hc rfl)

theorem efrc_raw_semantics (op : UfrsOp) (a b c d : ℤ)
    (hb : b ≠ 0) (hd : d ≠ 0) (hc : op = .div → c ≠ 0) :
    ((efrcRaw op a b c d).1 : ℚ) / ((efrcRaw op a b c d).2 : ℚ) =
      ufrsExact op ((a : ℚ)/b) ((c : ℚ)/d) := by
  have hbq : (b : ℚ) ≠ 0 := by exact_mod_cast hb
  have hdq : (d : ℚ) ≠ 0 := by exact_mod_cast hd
  cases op
  · simp only [efrcRaw, ufrsExact, Int.cast_add, Int.cast_mul]
    field_simp
    <;> ring
  · simp only [efrcRaw, ufrsExact, Int.cast_sub, Int.cast_mul]
    field_simp
    <;> ring
  · simp only [efrcRaw, ufrsExact, Int.cast_mul]
    field_simp
  · have hcq : (c : ℚ) ≠ 0 := by exact_mod_cast hc rfl
    simp only [efrcRaw, ufrsExact, Int.cast_mul]
    field_simp
    <;> ring

theorem efrc_uniform_reduced_budget (op : UfrsOp) (a b c d : ℤ)
    (n m k l B : ℕ)
    (ha : EfrcFits a.natAbs n) (hb : EfrcFits b.natAbs m)
    (hc : EfrcFits c.natAbs k) (hd : EfrcFits d.natAbs l)
    (hB : efrcCost op n m k l ≤ B) :
    let u := (efrcRaw op a b c d).1.natAbs
    let v := (efrcRaw op a b c d).2.natAbs
    EfrcFits (u / Nat.gcd u v) B ∧ EfrcFits (v / Nat.gcd u v) B := by
  obtain ⟨hu,hv⟩ := efrc_raw_budget op a b c d n m k l B ha hb hc hd hB
  exact efrc_gcd_budget _ _ B hu hv

end CLUIOT

namespace CLUIOT

noncomputable def efrcPoly : List ℚ → Polynomial ℚ
  | [] => 0
  | c :: cs => Polynomial.C c + Polynomial.X * efrcPoly cs

def efrcHorner (x : ℚ) : List ℚ → ℚ
  | [] => 0
  | c :: cs => c + x * efrcHorner x cs

theorem efrc_poly_eval (x : ℚ) (cs : List ℚ) :
    (efrcPoly cs).eval x = efrcHorner x cs := by
  induction cs with
  | nil => simp [efrcPoly, efrcHorner]
  | cons c cs ih => simp [efrcPoly, efrcHorner, ih]

theorem efrc_poly_trailing_zero (cs : List ℚ) :
    efrcPoly (cs ++ [0]) = efrcPoly cs := by
  induction cs with
  | nil => simp [efrcPoly]
  | cons c cs ih => simp [efrcPoly, ih]

theorem efrc_poly_literal (c : ℚ) :
    efrcPoly [c] = Polynomial.C c := by simp [efrcPoly]

theorem efrc_poly_variable :
    efrcPoly [0,1] = (Polynomial.X : Polynomial ℚ) := by
  simp [efrcPoly]

end CLUIOT
