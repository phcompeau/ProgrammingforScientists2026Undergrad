# UPGMA Tree Teaching Notes

Eight datasets, each showing a different biological story that UPGMA + edit distance can reveal.
One paragraph of instructor talking points per dataset.

---

## 1. HBA1 — Vertebrate Hemoglobin Alpha (108 taxa)

**The story:** Vertebrate phylogeny at a glance — fish at the base, amphibians and reptiles next, then birds, then mammals. Within mammals, primates (including humans) form a tight cluster, while rodents, carnivores, and ungulates form their own groups.

**What to explain:**
- Hemoglobin alpha is under strong functional constraint (it must bind oxygen), so it evolves slowly and acts as a reliable molecular clock — this is why UPGMA works well here.
- The tree should broadly match what students learned in intro bio: the vertebrate "tree of life." Point to specific features: ray-finned fish (Actinopterygii) near the root; tetrapods (amphibians, reptiles, birds, mammals) form a clade; within mammals, primates are most closely related to each other.
- **Limitation to acknowledge:** UPGMA assumes a strict molecular clock (all lineages evolve at the same rate). In reality, some lineages evolve faster than others. The tree may not perfectly match the accepted vertebrate phylogeny — for example, some fast-evolving lineages like rodents can appear artificially "basal."
- **Technical note:** With 108 sequences, this is the largest dataset. Each internal node represents a hypothetical common ancestor at the computed divergence time (age = half the edit distance at time of merger).

---

## 2. UK SARS-CoV-2 — Spike Protein Over Time (261 genomes, 2020–2024)

**The story:** The SARS-CoV-2 spike protein evolved dramatically over the pandemic. Early UK strains (2020) cluster together at the base, while later variants — Alpha, Delta, Omicron — each form their own distinct branches as they accumulated mutations that allowed them to evade immunity and spread more efficiently.

**What to explain:**
- This dataset uses time as a proxy for evolution: samples are labeled by collection date (YYYY-MM-DD). Students should see that sequences collected close in time cluster close together on the tree — this is the molecular clock at work for a rapidly evolving RNA virus.
- The spike protein is the gene that encodes the part of the virus that binds the ACE2 receptor on human cells and is the primary target of vaccines. New variants accumulate mutations in spike that allow them to escape prior immunity — this is why boosters were needed.
- Point out the large branch length separating Omicron (late 2021 onward) from earlier strains: Omicron accumulated an unusually large number of spike mutations, believed to have evolved in an immunocompromised patient or in an animal reservoir.
- **Technical note:** The samples at each time point are from real patient sequences deposited in public databases. Students are seeing actual evolutionary history from a pandemic they lived through.

---

## 3. Cytochrome C — Cross-Kingdom Eukaryotes (16 species)

**The story:** A single electron-carrier protein, cytochrome c (~104–112 amino acids), tells the deep story of eukaryotic evolution: fungi and plants are outgroups to animals, and within animals, mammals cluster together with primates most closely related to each other.

**What to explain:**
- Cytochrome c is one of the most evolutionarily conserved proteins known — yeast and human cytochrome c differ by ~44 amino acids out of ~104, yet the yeast protein can partially substitute for the human one in cell culture. This high conservation reflects extreme functional constraint: every amino acid matters for electron transport.
- The tree shows the classic eukaryote relationships: Saccharomyces (yeast) and Neurospora (bread mold) are fungi and sit far from animals; Arabidopsis (plant) is further still. Within animals, Xenopus (frog) and Danio (zebrafish) diverge first, then chicken, and mammals cluster together.
- **Highlight the primates:** Human and chimpanzee cytochrome c are *identical* — zero differences — which is why they share a branch of length zero at the tip. This is biologically meaningful: cytochrome c is under such strong purifying selection that even 5–6 million years of divergence left no amino acid changes.
- **Key concept:** This dataset illustrates that different genes evolve at different rates. Cytochrome c evolves slowly (hundreds of millions of years of divergence are visible), while spike protein (dataset 2) evolves fast enough that years of change are visible.

---

## 4. FOXP2 — The "Language Gene" in Great Apes and Songbirds (9 species)

**The story:** FOXP2 is the only gene where mutations cause a specific speech and language deficit in humans. The phylogeny shows the standard great ape tree (humans, chimps, gorillas, orangutans), but with a surprising outgroup: the zebra finch — a songbird whose FOXP2 is essential for learning songs, just as human FOXP2 is essential for learning speech.

**What to explain:**
- Humans and chimpanzees differ by only 2 amino acids in FOXP2 protein (~716 amino acids total), yet these changes are thought to be under strong positive selection in the human lineage and may contribute to our capacity for articulate speech. A family with a mutated FOXP2 has severe difficulty with the fine motor control needed for speech.
- The zebra finch inclusion is a teaching moment about convergent molecular evolution: birds and mammals independently evolved reliance on FOXP2 for vocal learning. Young zebra finches with disrupted FOXP2 cannot properly imitate their father's song. This parallel function suggests FOXP2 plays a deep role in the neural circuits for learned vocalization.
- The tree should show the correct great ape topology: ((Human, Chimp), Gorilla, Orangutan) with macaque as outgroup. Humans and chimps should cluster most closely together (edit distance ~2), separated from gorillas (which differ by more), and both far from the zebra finch.
- **Limitation:** Because humans and chimps are so similar (distance 2 in a ~716 aa protein), their branching order relative to gorillas depends on a single amino acid difference. If the tree shows humans closer to gorillas than chimps, point this out as a case where the molecular clock assumption fails for very closely related species.

---

## 5. Giant Panda and Bears (10 species)

**The story:** For decades, the giant panda's evolutionary placement was one of the most debated questions in mammalian systematics — was it a bear, a relative of the red panda, or its own lineage? Molecular data settled the debate: the giant panda is a true bear (Ursidae), while the red panda belongs to its own distinct family.

**What to explain:**
- Morphologically, the giant panda and red panda look similar (both eat bamboo, both have a "false thumb") and were historically grouped together. But the false thumb is a case of convergent evolution — it evolved independently in both lineages to help grip bamboo stalks.
- The cytochrome b tree places the giant panda squarely within the bear family (Ursidae), closest to spectacled bear, black bear, brown bear, and polar bear. The red panda appears as an outgroup, far from the bears.
- **Highlight polar and brown bears:** These two species show very small edit distances, reflecting relatively recent common ancestry (~500,000 years ago) and even occasional hybridization ("pizzly bears"). Students can see this in the short branch lengths.
- The spectacled bear (Tremarctos ornatus, found in South America) is the most basal true bear — it serves as the outgroup within Ursidae, consistent with the accepted phylogeny.
- **Key concept:** This dataset shows how molecular phylogenetics resolved a long-standing morphological controversy. When morphology misleads (due to convergent evolution), sequence data provides an independent and often decisive answer.

---

## 6. Cetaceans — Whales Within the Even-Toed Ungulates (12 species)

**The story:** Molecular phylogenetics revealed one of the most counterintuitive relationships in all of vertebrate biology: whales and dolphins did not merely branch off from hoofed mammals — they evolved from *within* the artiodactyls (even-toed ungulates). More specifically, the hippopotamus is more closely related to whales than it is to other ungulates like cows, pigs, or deer.

**What to explain:**
- Based on morphology alone, biologists grouped whales separately from all land mammals, because their body plan is so derived (no hind limbs, flukes, blowholes). But cytochrome b sequences tell a different story: hippos and whales cluster together, both sitting within a clade that includes pigs, deer, cattle, and camels.
- The fossil record now supports this: Pakicetus (~50 million years ago) was a four-legged artiodactyl that was the ancestor of modern whales. The transition from land to water happened within the artiodactyl lineage.
- The horse, rhinoceros, and elephant serve as outgroups in this tree (they are not artiodactyls). Students can verify that cetaceans (whale, dolphin) cluster with the artiodactyls, not with the horse or rhino.
- **Key concept:** This is a classic example of why molecular evidence revolutionized our understanding of mammalian evolution. Morphological characters can be misleading when a lineage undergoes extreme ecological and anatomical transformation.

---

## 7. HIV Subtypes — Pandemic Origins (10 strains)

**The story:** HIV-1 Group M caused the global AIDS pandemic after a single transmission of SIVcpz (chimpanzee SIV) to humans, probably in the 1920s in Central Africa. HIV-2, a less virulent virus, arose from a completely independent transmission of SIVsm from sooty mangabeys. The phylogeny shows all of this — multiple origins, subtypes reflecting geographic spread, and SIVcpz as the root.

**What to explain:**
- SIVcpz (chimpanzee SIV) is the most distantly related sequence and serves as the evolutionary root — HIV-1 is literally a mutated form of a chimpanzee virus that jumped to humans. SIVcpz sequences from chimps in central Africa are the closest known relatives of HIV-1.
- HIV-1 Group M subtypes (A, B, C, D, G) represent the virus that spread globally: subtype B is the predominant strain in North America and Western Europe; subtype C is the most common globally (dominant in sub-Saharan Africa and India). These subtypes arose as the virus spread through different populations and accumulated different mutations.
- HIV-1 Groups O and N are "outlier" clades from rare, independent cross-species transmissions. They cause AIDS but are much rarer than Group M.
- HIV-2 A and B are a completely separate branch — their ancestor is SIVsm, not SIVcpz. This is why HIV-2 causes milder disease and responds to different antiretroviral drugs.
- **Key concept:** Phylogenetics can be used in forensic contexts — when investigators need to determine whether one person infected another with HIV, they can compare viral sequences to see if one patient's virus is a direct descendant of the other's. This has been used in criminal cases and outbreak investigations.

---

## 8. Mitochondrial Haplogroups — Out of Africa (12 haplogroups)

**The story:** Human mitochondrial DNA is inherited maternally without recombination, so mutations accumulate along strictly maternal lineages. The resulting phylogeny maps human migration out of Africa: L0 (southern Africa) is the oldest lineage (~200,000 years ago); L3 (East Africa, ~70,000 years ago) is the ancestor of every non-African human alive today.

**What to explain:**
- The tree shows L0 (South Africa) as the root and oldest lineage, with L2 (Mozambique) branching next. Together, these are the deepest African lineages — found almost exclusively in sub-Saharan Africa. This pattern is the genetic evidence for the "Out of Africa" hypothesis: human genetic diversity is greatest in Africa, with African lineages at the base of the tree.
- L3 (Sudan) is the critical branch point: it is the last common maternal ancestor of all humans who left Africa. Above L3 in the tree, all haplogroups are non-African. This node represents the founding population that crossed into Eurasia.
- Non-Africans split into two major clades: the **M clade** (M, D, C) — dominant in South and East Asia and brought to the Americas — and the **N sub-clade** (H, J, U in Europe; A, X, B in the Americas and Pacific). Students can see these two clades as distinct clusters above L3.
- **Highlight the Americas:** The Americas haplogroups (A, B, C, D, and X) arrived via Beringia ~15,000–20,000 years ago. Students can see in the tree that A and B are in the N sub-clade while C is in the M clade — consistent with multiple founding haplogroups bringing both M and N lineages to the New World.
- **Limitation to acknowledge:** UPGMA groups sequences by overall sequence similarity, not by shared derived characters. The L0 lineage is ancient and has diverged from everyone — its edit distance to non-Africans (~70) is similar to its distance to L2 (~71). This means UPGMA cannot perfectly recover the fact that L0 is *more* closely related to L2 than to any non-African lineage in a strict cladistic sense. However, the tree still correctly shows L3 clustering with all non-Africans, which is the core biological result. For a more accurate reconstruction, one would need neighbor-joining or maximum likelihood methods that account for rate variation.
