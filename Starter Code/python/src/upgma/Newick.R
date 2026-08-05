# ─────────────────────────────────────────────────────────────────────────────
# UPGMA Tree Visualizations — ggtree pipeline
# Produces colored PNG figures for 8 biological datasets
# Run from the upgma/ directory (set Session > Set Working Directory > Source)
# ─────────────────────────────────────────────────────────────────────────────

# 1. Package setup ─────────────────────────────────────────────────────────────
for (pkg in c("ape", "ggplot2", "dplyr", "tibble")) {
  if (!requireNamespace(pkg, quietly = TRUE)) install.packages(pkg)
  library(pkg, character.only = TRUE)
}
if (!requireNamespace("ggtree", quietly = TRUE)) {
  if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  options(install.packages.compile.from.source = "never")
  BiocManager::install("ggtree", ask = FALSE)
}
library(ggtree)

# 2. Color palette ─────────────────────────────────────────────────────────────
RED    <- "#C94040"
ORANGE <- "#E07B39"
GOLD   <- "#E8B84B"
GREEN  <- "#5BAD72"
BLUE   <- "#5B8FCC"
PURPLE <- "#9B6FCA"
TEAL   <- "#4AACB0"
PINK   <- "#C96BA0"

# 3. Helpers ───────────────────────────────────────────────────────────────────

# Replace underscores with spaces
clean_label <- function(x) gsub("_", " ", x)

# Extract common name: everything after the first two underscores
common_name <- function(x) {
  parts <- strsplit(x, "_")[[1]]
  if (length(parts) <= 2) return(gsub("_", " ", x))
  paste(parts[3:length(parts)], collapse = " ")
}

# Core rendering function
render_tree <- function(
    newick_path, output_path,
    group_map,              # named character vector: tip_label -> group name
    palette,                # named character vector: group name -> hex color
    width        = 14,      # figure width in inches
    height       = 10,      # figure height in inches
    tip_size     = 3.5,     # label font size
    point_size   = 5,       # tip point size
    show_labels  = TRUE,
    layout       = "rectangular",
    label_fn     = clean_label,
    label_expand = 1.7,     # x-axis multiplier for rectangular layout only
    legend_text_size = 16,  # legend text size in pt
    legend_key_size  = 1.2  # legend key size in cm
) {
  tree <- read.tree(newick_path)

  meta <- tibble(
    label   = tree$tip.label,
    display = sapply(label, label_fn),
    group   = group_map[label]
  )
  meta$group[is.na(meta$group)] <- "Other"

  all_colors <- c(palette, Other = "gray60")
  grp_order  <- c(names(palette), if ("Other" %in% meta$group) "Other")

  # Base tree with metadata joined
  p <- ggtree(tree, color = "gray35", linewidth = 0.7, layout = layout) %<+% meta

  # Tip points
  p <- p + geom_tippoint(aes(color = group), size = point_size, alpha = 0.95)

  # Tip labels (skip xlim expansion for circular layout)
  if (show_labels) {
    p <- p + geom_tiplab(aes(label = display, color = group),
                         size = tip_size, hjust = -0.1, fontface = "bold")
    if (layout != "circular") {
      tree_depth <- max(ape::node.depth.edgelength(tree))
      p <- p + xlim(0, tree_depth * label_expand)
    }
  }

  # Color scale + theme
  p <- p +
    scale_color_manual(values = all_colors, name = NULL,
                       breaks = grp_order, na.value = "gray60") +
    theme_tree() +
    theme(
      legend.text      = element_text(size = legend_text_size),
      legend.key.size  = unit(legend_key_size, "cm"),
      legend.position  = "right",
      plot.background  = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA)
    )

  dir.create(dirname(output_path), showWarnings = FALSE, recursive = TRUE)
  ggsave(output_path, p, width = width, height = height, dpi = 200, bg = "white")
  message("Saved: ", output_path)
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. Dataset configs
# ─────────────────────────────────────────────────────────────────────────────

# ── 4a. HBA1: Vertebrate Hemoglobin (108 taxa, circular layout) ───────────────
{
  primates <- c(
    "Homo_sapiens_Human", "Pan_paniscus_Bonobo", "Pan_troglodytes_Chimpanzee",
    "Pongo_pygmaeus_Bornean_orangutan", "Pongo_abelii_Sumatran_orangutan",
    "Hylobates_lar_Lar_gibbon", "Macaca_mulatta_Rhesus_macaque",
    "Papio_anubis_Olive_baboon", "Plecturocebus_moloch_Silvery_marmoset",
    "Varecia_variegata_Lemur", "Hapalemur_griseus_Eastern_lesser_bamboo_lemur"
  )
  birds <- c(
    "Coscoroba_coscoroba_Coscoroba_swan", "Cereopsis_novaehollandiae_Cape_Barren_goose",
    "Branta_bernicla_Brent_goose", "Anser_indicus_Bar-headed_goose",
    "Anser_canagicus_Emperor_goose", "Anser_fabalis_Bean_goose",
    "Branta_canadensis_Canada_goose", "Branta_sandvicensis_Nene",
    "Anser_cygnoides_Swan_goose", "Branta_leucopsis_Barnacle_goose",
    "Anser_anser_Greylag_goose", "Anser_albifrons_White-fronted_goose",
    "Anser_rossii_Rosss_goose", "Anser_caerulescens_Snow_goose",
    "Cygnus_melancoryphus_Black-necked_swan", "Cygnus_buccinator_Trumpeter_swan",
    "Cygnus_columbianus_Tundra_swan", "Cygnus_atratus_Black_swan",
    "Cygnus_olor_Mute_swan", "Tadorna_tadornoides_Australian_shelduck",
    "Neochen_jubata_Orinoco_goose", "Chloephaga_melanoptera_Andean_goose",
    "Chloephaga_hybrida_malvinarum_Kelp_goose",
    "Chloephaga_picta_leucoptera_Southern_shelduck",
    "Chloephaga_poliocephala_Ashy-headed_goose",
    "Chloephaga_rubidiceps_Ruddy-headed_goose",
    "Chenonetta_jubata_Maned_duck", "Melanitta_fusca_Velvet_scoter",
    "Somateria_fischeri_Spectacled_eider", "Somateria_spectabilis_King_eider",
    "Clangula_hyemalis_Long-tailed_duck", "Callonetta_leucophrys_Ringed_teal",
    "Biziura_lobata_Musk_duck", "Dendrocygna_eytoni_Plumed_whistling_duck",
    "Malacorhynchus_membranaceus_Pink-eared_duck",
    "Oxyura_ferruginea_Andean_duck", "Oxyura_vittata_Lake_duck",
    "Oxyura_jamaicensis_jamaicensis_Ruddy_duck", "Nomonyx_dominicus_Masked_duck",
    "Herpetotheres_cachinnans_Laughing_falcon", "Ibidorhyncha_struthersii_Ibisbill",
    "Alca_torda_Razorbill", "Cepphus_grylle_Black_guillemot",
    "Dromas_ardeola_Crab-plover", "Stercorarius_maccormicki_South_Polar_Skua",
    "Chionis_minor_Black-faced_sheathbill", "Nycticryphes_semicollaris_Night_parrot",
    "Himantopus_himantopus_Black-winged_stilt"
  )
  rept_amph <- c(
    "Xenopus_laevis_African_clawed_frog", "Xenopus_tropicalis_Western_clawed_frog",
    "Pleurodeles_waltl_Iberian_ribbed_newt",
    "Aldabrachelys_gigantea_Seychelles_giant_tortoise",
    "Iguana_iguana_Iguana", "Naja_naja_Indian_cobra"
  )
  fish <- c(
    "Torpedo_marmorata_Marbled_electric_ray",
    "Sphoeroides_nephelus_Southern_puffer", "Oncorhynchus_mykiss_Rainbow_trout",
    "Liparis_tanakae_Tanakas_snailfish", "Liparis_tunicatus_Kelp_snailfish",
    "Trematomus_newnesi_Emerald_rockcod", "Gobionotothen_gibberifrons_Humped_rockcod",
    "Notothenia_angustata_Black_cod", "Arctogadus_glacialis_Arctic_cod",
    "Gadus_morhua_Atlantic_cod", "Anoplopoma_fimbria_Sablefish",
    "Anarhichas_minor_Spotted_wolffish"
  )
  hba1_gmap <- c(
    setNames(rep("Primates",              length(primates)),   primates),
    setNames(rep("Birds",                 length(birds)),      birds),
    setNames(rep("Reptiles & Amphibians", length(rept_amph)), rept_amph),
    setNames(rep("Fish",                  length(fish)),       fish)
  )
  render_tree(
    newick_path  = "Output/HBA1/hba1.tre",
    output_path  = "Output/Images/01_HBA1.png",
    group_map    = hba1_gmap,
    palette      = c("Primates"              = RED,
                     "Birds"                 = BLUE,
                     "Reptiles & Amphibians" = GREEN,
                     "Fish"                  = TEAL),
    width = 20, height = 42, tip_size = 2.5, point_size = 3.5,
    show_labels = TRUE, label_fn = common_name, label_expand = 1.5,
    legend_text_size = 48, legend_key_size = 3
  )
}

# ── 4b. UK SARS-CoV-2: Coronavirus over time (261 taxa, no labels) ───────────
{
  tree_sars  <- read.tree("Output/UK-SARS-CoV-2/sars.tre")
  years      <- substr(tree_sars$tip.label, 1, 4)
  covid_gmap <- setNames(years, tree_sars$tip.label)
  render_tree(
    newick_path  = "Output/UK-SARS-CoV-2/sars.tre",
    output_path  = "Output/Images/02_COVID.png",
    group_map    = covid_gmap,
    palette      = c("2020" = GREEN,
                     "2021" = BLUE,
                     "2022" = PURPLE,
                     "2023" = ORANGE,
                     "2024" = RED),
    width = 14, height = 28, point_size = 3, show_labels = FALSE
  )
}

# ── 4c. Cytochrome-C: Same protein across all of life ────────────────────────
{
  cyto_gmap <- c(
    Homo_sapiens_Human               = "Primates",
    Pan_troglodytes_Chimpanzee       = "Primates",
    Gorilla_gorilla_Gorilla          = "Primates",
    Pongo_pygmaeus_Orangutan         = "Primates",
    Macaca_mulatta_Rhesus_monkey     = "Primates",
    Bos_taurus_Cow                   = "Mammals",
    Sus_scrofa_Pig                   = "Mammals",
    Equus_caballus_Horse             = "Mammals",
    Mus_musculus_Mouse               = "Mammals",
    Canis_familiaris_Dog             = "Mammals",
    Gallus_gallus_Chicken            = "Birds & Amphibians",
    Xenopus_laevis_Frog              = "Birds & Amphibians",
    Danio_rerio_Zebrafish            = "Fish",
    Saccharomyces_cerevisiae_Yeast   = "Fungi",
    Neurospora_crassa_Bread_mold     = "Fungi",
    Arabidopsis_thaliana_Arabidopsis = "Plants"
  )
  render_tree(
    newick_path  = "Output/Cytochrome-C/cytochrome_c.tre",
    output_path  = "Output/Images/03_CytochromeC.png",
    group_map    = cyto_gmap,
    palette      = c("Primates"           = RED,
                     "Mammals"            = ORANGE,
                     "Birds & Amphibians" = BLUE,
                     "Fish"               = TEAL,
                     "Fungi"              = PURPLE,
                     "Plants"             = GREEN),
    label_fn = common_name, label_expand = 1.8
  )
}

# ── 4d. Great Apes FOXP2: The speech gene ────────────────────────────────────
{
  foxp2_gmap <- c(
    Homo_sapiens_Human             = "Humans",
    Pan_troglodytes_Chimpanzee     = "Great Apes",
    Pan_paniscus_Bonobo            = "Great Apes",
    Gorilla_gorilla_Gorilla        = "Great Apes",
    Pongo_abelii_Orangutan         = "Great Apes",
    Nomascus_leucogenys_Gibbon     = "Great Apes",
    Macaca_mulatta_Rhesus_monkey   = "Old World Monkeys",
    Mus_musculus_Mouse             = "Rodents",
    Taeniopygia_guttata_Zebrafinch = "Birds"
  )
  render_tree(
    newick_path  = "Output/Great-Apes-FOXP2/great_apes.tre",
    output_path  = "Output/Images/04_FOXP2.png",
    group_map    = foxp2_gmap,
    palette      = c("Humans"            = RED,
                     "Great Apes"        = ORANGE,
                     "Old World Monkeys" = GOLD,
                     "Rodents"           = PURPLE,
                     "Birds"             = BLUE),
    label_fn = common_name, label_expand = 1.9
  )
}

# ── 4e. Giant Panda & Bears (raccoon removed) ─────────────────────────────────
{
  panda_gmap <- c(
    Ailuropoda_melanoleuca_Giant_panda   = "Giant Panda",
    Ursus_maritimus_Polar_bear           = "True Bears",
    Ursus_americanus_American_black_bear = "True Bears",
    Ursus_arctos_Brown_bear              = "True Bears",
    Ursus_thibetanus_Asiatic_black_bear  = "True Bears",
    Helarctos_malayanus_Sun_bear         = "True Bears",
    Tremarctos_ornatus_Spectacled_bear   = "True Bears",
    Ailurus_fulgens_Red_panda            = "Red Panda",
    Mustela_putorius_Ferret              = "Ferret"
  )
  render_tree(
    newick_path  = "Output/Giant-Panda-Bears/giant_panda.tre",
    output_path  = "Output/Images/05_GiantPanda.png",
    group_map    = panda_gmap,
    palette      = c("Giant Panda" = RED,
                     "True Bears"  = BLUE,
                     "Red Panda"   = ORANGE,
                     "Ferret"      = PURPLE),
    label_fn = common_name, label_expand = 1.9
  )
}

# ── 4f. Cetaceans: Whales are swimming artiodactyls ──────────────────────────
# Story: cetaceans (blue) are nested INSIDE even-toed ungulates, with hippo
# as their closest living relative — one of evolution's biggest surprises.
{
  cet_gmap <- c(
    Tursiops_truncatus_Bottlenose_dolphin = "Cetaceans",
    Orcinus_orca_Killer_whale             = "Cetaceans",
    Balaenoptera_musculus_Blue_whale      = "Cetaceans",
    Physeter_macrocephalus_Sperm_whale    = "Cetaceans",
    Hippopotamus_amphibius_Hippopotamus   = "Hippo (closest to whales)",
    Sus_scrofa_Pig                        = "Artiodactyls",
    Bos_taurus_Cow                        = "Artiodactyls",
    Giraffa_camelopardalis_Giraffe        = "Artiodactyls",
    Camelus_dromedarius_Dromedary         = "Artiodactyls",
    Equus_caballus_Horse                  = "Odd-toed Ungulates",
    Rhinoceros_unicornis_Rhinoceros       = "Odd-toed Ungulates",
    Loxodonta_africana_African_elephant   = "Elephant (outgroup)"
  )
  render_tree(
    newick_path  = "Output/Cetaceans/cetaceans.tre",
    output_path  = "Output/Images/06_Cetaceans.png",
    group_map    = cet_gmap,
    palette      = c("Cetaceans"              = BLUE,
                     "Hippo (closest to whales)" = GREEN,
                     "Artiodactyls"           = GOLD,
                     "Odd-toed Ungulates"     = ORANGE,
                     "Elephant (outgroup)"    = PURPLE),
    label_fn = common_name, label_expand = 1.9
  )
}

# ── 4g. HIV Subtypes: Origins of a pandemic ───────────────────────────────────
# Updated group_map — will be extended once new SIV data is built
{
  hiv_gmap <- c(
    "HIV-1_GroupM_SubtypeA_Q23"     = "HIV-1 Group M (chimp origin)",
    "HIV-1_GroupM_SubtypeB_HXB2"    = "HIV-1 Group M (chimp origin)",
    "HIV-1_GroupM_SubtypeC_ETH2220" = "HIV-1 Group M (chimp origin)",
    "HIV-1_GroupM_SubtypeD_NDK"     = "HIV-1 Group M (chimp origin)",
    "HIV-1_GroupM_SubtypeG_SE6165"  = "HIV-1 Group M (chimp origin)",
    "HIV-1_GroupN_YBF30"            = "HIV-1 Group N (chimp origin)",
    "HIV-1_GroupO_ANT70"            = "HIV-1 Group O (gorilla origin)",
    "HIV-1_GroupP_RBF168"           = "HIV-1 Group P (gorilla origin)",
    "HIV-2_GroupA_ROD"              = "HIV-2 (mangabey origin)",
    "HIV-2_GroupB_EHO"              = "HIV-2 (mangabey origin)",
    "SIVcpz_Tanzania"               = "SIV (chimpanzee)",
    "SIVgor_Cameroon"               = "SIV (gorilla)",
    "SIVsm_SootyMangabey"           = "SIV (sooty mangabey)",
    "SIVrcm_RedCapMangabey"         = "SIV (other primate)"
  )
  hiv_label <- function(x) {
    x <- sub("HIV-1_GroupM_Subtype([A-Z])_.*", "HIV-1 M:Sub\\1",   x)
    x <- sub("HIV-1_GroupN_.*",                "HIV-1 Group N",     x)
    x <- sub("HIV-1_GroupO_.*",                "HIV-1 Group O",     x)
    x <- sub("HIV-1_GroupP_.*",                "HIV-1 Group P",     x)
    x <- sub("HIV-2_Group([AB])_.*",           "HIV-2 Group \\1",   x)
    x <- sub("SIVcpz_Tanzania",                "SIVcpz (Tanzania)", x)
    x <- sub("SIVgor_Cameroon",                "SIVgor (Cameroon)", x)
    x <- sub("SIVsm_SootyMangabey",            "SIVsm (mangabey)",  x)
    x <- sub("SIVrcm_RedCapMangabey",          "SIVrcm (mangabey)", x)
    x
  }
  render_tree(
    newick_path  = "Output/HIV-Subtypes/hiv.tre",
    output_path  = "Output/Images/07_HIV.png",
    group_map    = hiv_gmap,
    palette      = c("HIV-1 Group M (chimp origin)"    = RED,
                     "HIV-1 Group N (chimp origin)"    = PINK,
                     "HIV-1 Group O (gorilla origin)"  = ORANGE,
                     "HIV-1 Group P (gorilla origin)"  = GOLD,
                     "HIV-2 (mangabey origin)"         = PURPLE,
                     "SIV (chimpanzee)"                = "#3a7a3a",
                     "SIV (gorilla)"                   = "#5aaa5a",
                     "SIV (sooty mangabey)"            = TEAL,
                     "SIV (other primate)"             = "#7bbcbc"),
    label_fn = hiv_label, label_expand = 2.2,
    height = 12
  )
}

# ── 4h. Mitochondrial Haplogroups: Out of Africa ──────────────────────────────
# haplo_gmap is built dynamically from sequence labels so it works for any
# number of sequences — group is determined by the haplogroup letter prefix.
{
  tree_hap   <- read.tree("Output/Mitochondrial-Haplogroups/haplogroups.tre")
  all_labels <- tree_hap$tip.label

  # Assign by leading haplogroup letter(s)
  assign_haplo_group <- function(lbl) {
    hap <- strsplit(lbl, "_")[[1]][1]
    if (grepl("^L0", hap))                        return("African L0 (oldest)")
    if (grepl("^L[123]|^L[^0]", hap))             return("African L1-L3")
    if (grepl("^[CD]", hap))                       return("Asian (M clade)")
    if (grepl("^[MGQ]|^M[0-9]", hap))             return("Asian (M clade)")
    if (grepl("^[AB]|^[FZ]", hap))                return("East Asian & Pacific")
    if (grepl("^[HJKTUVI]|^U[0-9]|^H[0-9]", hap)) return("European")
    if (grepl("^[NWX]", hap))                      return("Middle Eastern / Ancient N")
    if (grepl("^R$", hap))                         return("European")
    return("Other")
  }
  haplo_gmap <- setNames(sapply(all_labels, assign_haplo_group), all_labels)

  haplo_label <- function(x) {
    parts      <- strsplit(x, "_")[[1]]
    haplogroup <- parts[1]
    location   <- if (length(parts) >= 3) parts[3] else ""
    paste0(haplogroup, " (", location, ")")
  }
  render_tree(
    newick_path  = "Output/Mitochondrial-Haplogroups/haplogroups.tre",
    output_path  = "Output/Images/08_Haplogroups.png",
    group_map    = haplo_gmap,
    palette      = c("African L0 (oldest)"       = "#8B1A1A",
                     "African L1-L3"             = RED,
                     "Asian (M clade)"           = GOLD,
                     "East Asian & Pacific"      = ORANGE,
                     "European"                  = BLUE,
                     "Middle Eastern / Ancient N"= TEAL,
                     "Other"                     = "gray60"),
    label_fn    = haplo_label, label_expand = 2.1,
    height = 14
  )
}

message("\nAll 8 trees rendered to Output/Images/")
