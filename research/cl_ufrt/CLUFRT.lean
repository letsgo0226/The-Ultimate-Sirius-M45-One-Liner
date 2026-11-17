/-!
CL-UFRT: a type-theoretic *representation*, not a universal solver.
Lean 4 core only; no mathlib, axioms, sorry, or external imports.
-/

universe u

namespace CLUFRT

def IsSolution {P : Type u} : P ⊕ PUnit → Prop
  | Sum.inl _ => True
  | Sum.inr _ => False

def SolFixed (P : Type u) : Type u :=
  { x : P ⊕ PUnit // (id x = x) ∧ IsSolution x }

def encode {P : Type u} (p : P) : SolFixed P :=
  ⟨Sum.inl p, ⟨rfl, True.intro⟩⟩

def decode {P : Type u} (s : SolFixed P) : P :=
  match s with
  | ⟨Sum.inl p, _⟩ => p
  | ⟨Sum.inr _, ⟨_, h⟩⟩ => False.elim h

theorem decode_encode {P : Type u} (p : P) :
    decode (encode p) = p := rfl

theorem encode_decode {P : Type u} (s : SolFixed P) :
    encode (decode s) = s := by
  cases s with
  | mk x h =>
    cases x with
    | inl p =>
      apply Subtype.ext
      rfl
    | inr u =>
      exact False.elim h.2

def equivalence (P : Type u) : P ≃ SolFixed P where
  toFun := encode
  invFun := decode
  left_inv := decode_encode
  right_inv := encode_decode

-- A witness of P is equivalent to a certified fixed point, not produced from nothing.
theorem inhabitation_iff (P : Type u) :
    Nonempty P ↔ Nonempty (SolFixed P) := by
  constructor
  · rintro ⟨p⟩
    exact ⟨encode p⟩
  · rintro ⟨s⟩
    exact ⟨decode s⟩

end CLUFRT
