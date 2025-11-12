#!/bin/bash
# Generate Dhātu module files

cd /home/stephane/GitHub/Panini-FS

echo "Creating Dhātu module: emotion.rs"
cat > crates/panini-core/src/dhatu/emotion.rs << 'EOFEMOTION'
//! Panksepp Emotional System
//!
//! Based on Jaak Panksepp's affective neuroscience research.
//! Seven primary emotional systems found across all mammals.

use serde::{Deserialize, Serialize};
use std::fmt;

/// Panksepp's seven primary emotional systems
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum PankseppEmotion {
    /// SEEKING: Exploration, curiosity, desire, dopamine-driven
    /// Sanskrit: icchā (इच्छा), kāṅkṣā (काङ्क्षा)
    Seeking,
    
    /// FEAR: Anxiety, vigilance, freezing, flight
    /// Sanskrit: bhaya (भय), bhīti (भीति)
    Fear,
    
    /// RAGE: Anger, frustration, irritation, assertion
    /// Sanskrit: krodha (क्रोध), manyū (मन्यू)
    Rage,
    
    /// LUST: Sexual desire, erotic arousal, reproduction
    /// Sanskrit: kāma (काम), rati (रति)
    Lust,
    
    /// CARE: Nurturing, compassion, maternal instinct, bonding
    /// Sanskrit: karuṇā (करुणा), sneha (स्नेह)
    Care,
    
    /// PANIC/GRIEF: Separation distress, loneliness, sadness
    /// Sanskrit: śoka (शोक), viṣāda (विषाद)
    PanicGrief,
    
    /// PLAY: Joyful engagement, roughhousing, social bonding
    /// Sanskrit: krīḍā (क्रीडा), līlā (लीला)
    Play,
}

impl PankseppEmotion {
    /// Get all seven emotions
    pub fn all() -> Vec<Self> {
        vec![
            Self::Seeking,
            Self::Fear,
            Self::Rage,
            Self::Lust,
            Self::Care,
            Self::PanicGrief,
            Self::Play,
        ]
    }
    
    /// Get Sanskrit name (primary)
    pub fn sanskrit_name(&self) -> &'static str {
        match self {
            Self::Seeking => "icchā",
            Self::Fear => "bhaya",
            Self::Rage => "krodha",
            Self::Lust => "kāma",
            Self::Care => "karuṇā",
            Self::PanicGrief => "śoka",
            Self::Play => "krīḍā",
        }
    }
    
    /// Get Devanagari script
    pub fn devanagari(&self) -> &'static str {
        match self {
            Self::Seeking => "इच्छा",
            Self::Fear => "भय",
            Self::Rage => "क्रोध",
            Self::Lust => "काम",
            Self::Care => "करुणा",
            Self::PanicGrief => "शोक",
            Self::Play => "क्रीडा",
        }
    }
    
    /// Get description
    pub fn description(&self) -> &'static str {
        match self {
            Self::Seeking => "Exploration, curiosity, desire, anticipation",
            Self::Fear => "Anxiety, vigilance, threat avoidance",
            Self::Rage => "Anger, frustration, assertion",
            Self::Lust => "Sexual desire, erotic arousal",
            Self::Care => "Nurturing, compassion, bonding",
            Self::PanicGrief => "Separation distress, loneliness",
            Self::Play => "Joyful engagement, social bonding",
        }
    }
    
    /// Get associated neurotransmitter
    pub fn neurotransmitter(&self) -> &'static str {
        match self {
            Self::Seeking => "Dopamine",
            Self::Fear => "Glutamate",
            Self::Rage => "Substance P",
            Self::Lust => "Testosterone/Estrogen",
            Self::Care => "Oxytocin",
            Self::PanicGrief => "Opioids (withdrawal)",
            Self::Play => "Endorphins",
        }
    }
    
    /// Get color for visualization (hex)
    pub fn color(&self) -> &'static str {
        match self {
            Self::Seeking => "#FFD700", // Gold
            Self::Fear => "#4B0082",    // Indigo
            Self::Rage => "#DC143C",    // Crimson
            Self::Lust => "#FF1493",    // Deep pink
            Self::Care => "#32CD32",    // Lime green
            Self::PanicGrief => "#4169E1", // Royal blue
            Self::Play => "#FF8C00",    // Dark orange
        }
    }
}

impl fmt::Display for PankseppEmotion {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{:?}", self)
    }
}

/// Emotional intensity score (0.0 - 1.0)
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct EmotionalIntensity {
    pub seeking: f64,
    pub fear: f64,
    pub rage: f64,
    pub lust: f64,
    pub care: f64,
    pub panic_grief: f64,
    pub play: f64,
}

impl EmotionalIntensity {
    pub fn new() -> Self {
        Self {
            seeking: 0.0,
            fear: 0.0,
            rage: 0.0,
            lust: 0.0,
            care: 0.0,
            panic_grief: 0.0,
            play: 0.0,
        }
    }
    
    pub fn get(&self, emotion: PankseppEmotion) -> f64 {
        match emotion {
            PankseppEmotion::Seeking => self.seeking,
            PankseppEmotion::Fear => self.fear,
            PankseppEmotion::Rage => self.rage,
            PankseppEmotion::Lust => self.lust,
            PankseppEmotion::Care => self.care,
            PankseppEmotion::PanicGrief => self.panic_grief,
            PankseppEmotion::Play => self.play,
        }
    }
    
    pub fn set(&mut self, emotion: PankseppEmotion, value: f64) {
        let value = value.clamp(0.0, 1.0);
        match emotion {
            PankseppEmotion::Seeking => self.seeking = value,
            PankseppEmotion::Fear => self.fear = value,
            PankseppEmotion::Rage => self.rage = value,
            PankseppEmotion::Lust => self.lust = value,
            PankseppEmotion::Care => self.care = value,
            PankseppEmotion::PanicGrief => self.panic_grief = value,
            PankseppEmotion::Play => self.play = value,
        }
    }
    
    /// Get dominant emotion (highest intensity)
    pub fn dominant(&self) -> Option<PankseppEmotion> {
        let emotions = vec![
            (PankseppEmotion::Seeking, self.seeking),
            (PankseppEmotion::Fear, self.fear),
            (PankseppEmotion::Rage, self.rage),
            (PankseppEmotion::Lust, self.lust),
            (PankseppEmotion::Care, self.care),
            (PankseppEmotion::PanicGrief, self.panic_grief),
            (PankseppEmotion::Play, self.play),
        ];
        
        emotions.into_iter()
            .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
            .filter(|(_, intensity)| *intensity > 0.0)
            .map(|(emotion, _)| emotion)
    }
    
    /// Overall emotional arousal (sum of all intensities)
    pub fn arousal(&self) -> f64 {
        self.seeking + self.fear + self.rage + self.lust 
            + self.care + self.panic_grief + self.play
    }
}

impl Default for EmotionalIntensity {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_emotions() {
        assert_eq!(PankseppEmotion::all().len(), 7);
    }

    #[test]
    fn test_emotional_intensity() {
        let mut intensity = EmotionalIntensity::new();
        intensity.set(PankseppEmotion::Seeking, 0.8);
        intensity.set(PankseppEmotion::Fear, 0.3);
        
        assert_eq!(intensity.dominant(), Some(PankseppEmotion::Seeking));
        assert_eq!(intensity.arousal(), 1.1);
    }
}
EOFEMOTION

echo "✅ emotion.rs created"

echo "Creating Dhātu module: root.rs"
cat > crates/panini-core/src/dhatu/root.rs << 'EOFROOT'
//! Sanskrit Dhātu (Root) System
//!
//! Dhātus are the fundamental verbal roots in Sanskrit grammar.
//! Each carries semantic and emotional resonance.

use serde::{Deserialize, Serialize};
use super::emotion::PankseppEmotion;
use std::collections::HashMap;

/// Sanskrit verbal root (dhātu)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DhatuRoot {
    /// Root in IAST transliteration
    pub root: String,
    
    /// Devanagari script
    pub devanagari: String,
    
    /// Primary meaning
    pub meaning: String,
    
    /// Associated Panksepp emotion
    pub emotion: PankseppEmotion,
    
    /// Emotional intensity (0.0 - 1.0)
    pub intensity: f64,
    
    /// Secondary meanings
    pub secondary_meanings: Vec<String>,
    
    /// Example words derived from this root
    pub derived_words: Vec<String>,
    
    /// Optional metadata
    #[serde(default)]
    pub metadata: HashMap<String, String>,
}

impl DhatuRoot {
    pub fn new(
        root: impl Into<String>,
        devanagari: impl Into<String>,
        meaning: impl Into<String>,
        emotion: PankseppEmotion,
        intensity: f64,
    ) -> Self {
        Self {
            root: root.into(),
            devanagari: devanagari.into(),
            meaning: meaning.into(),
            emotion,
            intensity: intensity.clamp(0.0, 1.0),
            secondary_meanings: Vec::new(),
            derived_words: Vec::new(),
            metadata: HashMap::new(),
        }
    }
    
    pub fn with_secondary(mut self, meanings: Vec<String>) -> Self {
        self.secondary_meanings = meanings;
        self
    }
    
    pub fn with_derived(mut self, words: Vec<String>) -> Self {
        self.derived_words = words;
        self
    }
}

/// Collection of canonical dhātu roots
pub struct DhatuCatalog {
    roots: HashMap<String, DhatuRoot>,
}

impl DhatuCatalog {
    pub fn new() -> Self {
        let mut catalog = Self {
            roots: HashMap::new(),
        };
        catalog.load_canonical_roots();
        catalog
    }
    
    /// Load canonical Sanskrit roots with emotional mapping
    fn load_canonical_roots(&mut self) {
        // SEEKING roots
        self.add(DhatuRoot::new(
            "iṣ", "इष्", "to desire, to wish", 
            PankseppEmotion::Seeking, 0.9
        ).with_derived(vec!["icchā".into(), "īṣṭa".into()]));
        
        self.add(DhatuRoot::new(
            "eṣ", "एष्", "to seek, to search", 
            PankseppEmotion::Seeking, 0.85
        ));
        
        self.add(DhatuRoot::new(
            "gav", "गव्", "to desire, to strive", 
            PankseppEmotion::Seeking, 0.8
        ));
        
        // FEAR roots
        self.add(DhatuRoot::new(
            "bhī", "भी", "to fear, to be afraid", 
            PankseppEmotion::Fear, 0.95
        ).with_derived(vec!["bhaya".into(), "bhīti".into()]));
        
        self.add(DhatuRoot::new(
            "tras", "त्रस्", "to tremble, to be frightened", 
            PankseppEmotion::Fear, 0.85
        ).with_derived(vec!["trāsa".into(), "trasta".into()]));
        
        // RAGE roots
        self.add(DhatuRoot::new(
            "krudh", "क्रुध्", "to be angry", 
            PankseppEmotion::Rage, 0.95
        ).with_derived(vec!["krodha".into(), "kruddha".into()]));
        
        self.add(DhatuRoot::new(
            "man", "मन्", "to be angry, to resent", 
            PankseppEmotion::Rage, 0.8
        ).with_derived(vec!["manyū".into(), "manyate".into()]));
        
        // LUST roots
        self.add(DhatuRoot::new(
            "kam", "कम्", "to desire, to love", 
            PankseppEmotion::Lust, 0.9
        ).with_derived(vec!["kāma".into(), "kānti".into()]));
        
        self.add(DhatuRoot::new(
            "ram", "रम्", "to delight, to enjoy", 
            PankseppEmotion::Lust, 0.85
        ).with_derived(vec!["rati".into(), "ramana".into()]));
        
        // CARE roots
        self.add(DhatuRoot::new(
            "kṛp", "कृप्", "to compassionate, to pity", 
            PankseppEmotion::Care, 0.95
        ).with_derived(vec!["karuṇā".into(), "kṛpā".into()]));
        
        self.add(DhatuRoot::new(
            "snih", "स्निह्", "to be affectionate", 
            PankseppEmotion::Care, 0.9
        ).with_derived(vec!["sneha".into(), "snigdha".into()]));
        
        // PANIC/GRIEF roots
        self.add(DhatuRoot::new(
            "śuc", "शुच्", "to grieve, to mourn", 
            PankseppEmotion::PanicGrief, 0.95
        ).with_derived(vec!["śoka".into(), "śucita".into()]));
        
        self.add(DhatuRoot::new(
            "viṣad", "विषद्", "to despond, to be dejected", 
            PankseppEmotion::PanicGrief, 0.9
        ).with_derived(vec!["viṣāda".into(), "viṣaṇṇa".into()]));
        
        // PLAY roots
        self.add(DhatuRoot::new(
            "krīḍ", "क्रीड्", "to play, to sport", 
            PankseppEmotion::Play, 0.95
        ).with_derived(vec!["krīḍā".into(), "krīḍita".into()]));
        
        self.add(DhatuRoot::new(
            "līl", "लील्", "to play, to sport freely", 
            PankseppEmotion::Play, 0.9
        ).with_derived(vec!["līlā".into(), "līlita".into()]));
    }
    
    fn add(&mut self, root: DhatuRoot) {
        self.roots.insert(root.root.clone(), root);
    }
    
    pub fn get(&self, root: &str) -> Option<&DhatuRoot> {
        self.roots.get(root)
    }
    
    pub fn get_by_emotion(&self, emotion: PankseppEmotion) -> Vec<&DhatuRoot> {
        self.roots.values()
            .filter(|r| r.emotion == emotion)
            .collect()
    }
    
    pub fn all(&self) -> Vec<&DhatuRoot> {
        self.roots.values().collect()
    }
    
    pub fn search(&self, query: &str) -> Vec<&DhatuRoot> {
        let query_lower = query.to_lowercase();
        self.roots.values()
            .filter(|r| {
                r.root.to_lowercase().contains(&query_lower)
                    || r.meaning.to_lowercase().contains(&query_lower)
                    || r.secondary_meanings.iter()
                        .any(|m| m.to_lowercase().contains(&query_lower))
            })
            .collect()
    }
}

impl Default for DhatuCatalog {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dhatu_catalog() {
        let catalog = DhatuCatalog::new();
        assert!(!catalog.all().is_empty());
        
        let seeking_roots = catalog.get_by_emotion(PankseppEmotion::Seeking);
        assert!(!seeking_roots.is_empty());
    }

    #[test]
    fn test_dhatu_search() {
        let catalog = DhatuCatalog::new();
        let results = catalog.search("desire");
        assert!(!results.is_empty());
    }
}
EOFROOT

echo "✅ root.rs created"

echo "All Dhātu core files generated!"
