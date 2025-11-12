#!/bin/bash
# Generate Dhātu classifier and profile modules

cd /home/stephane/GitHub/Panini-FS

echo "Creating classifier.rs..."
cat > crates/panini-core/src/dhatu/classifier.rs << 'EOFCLASSIFIER'
//! Emotional Classification System
//!
//! Automatically classify files and content by emotional resonance

use super::emotion::{EmotionalIntensity, PankseppEmotion};
use super::root::{DhatuCatalog, DhatuRoot};
use anyhow::Result;
use std::path::Path;

/// Emotional classifier for files and content
pub struct DhatuClassifier {
    catalog: DhatuCatalog,
    keywords: KeywordMap,
}

/// Keyword mapping for emotional classification
struct KeywordMap {
    seeking: Vec<String>,
    fear: Vec<String>,
    rage: Vec<String>,
    lust: Vec<String>,
    care: Vec<String>,
    panic_grief: Vec<String>,
    play: Vec<String>,
}

impl KeywordMap {
    fn new() -> Self {
        Self {
            seeking: vec![
                "explore", "discover", "search", "quest", "adventure", "curiosity",
                "goal", "achieve", "progress", "develop", "create", "build",
                "research", "investigate", "analyze", "study", "learn",
            ].into_iter().map(String::from).collect(),
            
            fear: vec![
                "danger", "threat", "risk", "unsafe", "warning", "alert",
                "security", "vulnerability", "attack", "defense", "protect",
                "caution", "careful", "anxious", "worry", "concern",
            ].into_iter().map(String::from).collect(),
            
            rage: vec![
                "angry", "frustrate", "annoy", "irritate", "conflict", "fight",
                "battle", "war", "aggressive", "hostile", "attack", "destroy",
                "hate", "rage", "furious", "mad",
            ].into_iter().map(String::from).collect(),
            
            lust: vec![
                "desire", "want", "passion", "love", "romantic", "intimate",
                "sexual", "erotic", "pleasure", "sensual", "attraction",
                "beautiful", "gorgeous", "sexy",
            ].into_iter().map(String::from).collect(),
            
            care: vec![
                "care", "nurture", "support", "help", "assist", "compassion",
                "kindness", "gentle", "tender", "protect", "guardian",
                "parent", "child", "family", "community", "together",
            ].into_iter().map(String::from).collect(),
            
            panic_grief: vec![
                "sad", "grief", "loss", "mourn", "sorrow", "pain",
                "alone", "lonely", "isolate", "separate", "miss", "absence",
                "cry", "tears", "despair", "depression", "melancholy",
            ].into_iter().map(String::from).collect(),
            
            play: vec![
                "play", "fun", "game", "joy", "happy", "laugh",
                "entertainment", "enjoy", "party", "celebrate", "festival",
                "humor", "joke", "comedy", "silly", "playful",
            ].into_iter().map(String::from).collect(),
        }
    }
    
    fn get(&self, emotion: PankseppEmotion) -> &Vec<String> {
        match emotion {
            PankseppEmotion::Seeking => &self.seeking,
            PankseppEmotion::Fear => &self.fear,
            PankseppEmotion::Rage => &self.rage,
            PankseppEmotion::Lust => &self.lust,
            PankseppEmotion::Care => &self.care,
            PankseppEmotion::PanicGrief => &self.panic_grief,
            PankseppEmotion::Play => &self.play,
        }
    }
}

impl DhatuClassifier {
    pub fn new() -> Self {
        Self {
            catalog: DhatuCatalog::new(),
            keywords: KeywordMap::new(),
        }
    }
    
    /// Classify content by emotional resonance
    pub fn classify_content(&self, content: &str) -> EmotionalIntensity {
        let content_lower = content.to_lowercase();
        let mut intensity = EmotionalIntensity::new();
        
        // Count keyword matches for each emotion
        for emotion in PankseppEmotion::all() {
            let keywords = self.keywords.get(emotion);
            let matches = keywords.iter()
                .filter(|kw| content_lower.contains(kw.as_str()))
                .count();
            
            // Normalize by content length and keyword count
            let score = (matches as f64 / keywords.len() as f64)
                .min(1.0);
            
            intensity.set(emotion, score);
        }
        
        intensity
    }
    
    /// Classify file by name, extension, and path
    pub fn classify_file(&self, path: &Path) -> EmotionalIntensity {
        let mut intensity = EmotionalIntensity::new();
        
        // Extract components
        let filename = path.file_name()
            .and_then(|n| n.to_str())
            .unwrap_or("");
        let extension = path.extension()
            .and_then(|e| e.to_str())
            .unwrap_or("");
        let path_str = path.to_str().unwrap_or("");
        
        let combined = format!("{} {} {}", filename, extension, path_str)
            .to_lowercase();
        
        // File type heuristics
        match extension {
            // Code/development -> SEEKING
            "rs" | "py" | "js" | "ts" | "java" | "c" | "cpp" | "go" => {
                intensity.set(PankseppEmotion::Seeking, 0.7);
            }
            
            // Security/crypto -> FEAR
            "key" | "cert" | "pem" | "sec" => {
                intensity.set(PankseppEmotion::Fear, 0.8);
            }
            
            // Logs/errors -> RAGE
            "log" | "err" => {
                if combined.contains("error") || combined.contains("fail") {
                    intensity.set(PankseppEmotion::Rage, 0.6);
                }
            }
            
            // Media -> PLAY or LUST
            "jpg" | "png" | "gif" | "mp4" | "mp3" | "wav" => {
                intensity.set(PankseppEmotion::Play, 0.5);
            }
            
            // Docs -> CARE (knowledge sharing)
            "md" | "txt" | "pdf" | "doc" => {
                intensity.set(PankseppEmotion::Care, 0.4);
            }
            
            _ => {}
        }
        
        // Path-based classification
        if combined.contains("test") || combined.contains("spec") {
            intensity.set(PankseppEmotion::Seeking, 0.6);
        }
        
        if combined.contains("backup") || combined.contains("archive") {
            intensity.set(PankseppEmotion::Care, 0.7);
        }
        
        if combined.contains("tmp") || combined.contains("cache") {
            intensity.set(PankseppEmotion::Fear, 0.3);
        }
        
        intensity
    }
    
    /// Get dhātu roots for a given emotion
    pub fn get_roots(&self, emotion: PankseppEmotion) -> Vec<&DhatuRoot> {
        self.catalog.get_by_emotion(emotion)
    }
    
    /// Search for dhātu roots
    pub fn search_roots(&self, query: &str) -> Vec<&DhatuRoot> {
        self.catalog.search(query)
    }
}

impl Default for DhatuClassifier {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_classify_content() {
        let classifier = DhatuClassifier::new();
        
        let text = "We are exploring new discoveries with curiosity and research";
        let intensity = classifier.classify_content(text);
        
        assert!(intensity.seeking > 0.0);
        assert_eq!(intensity.dominant(), Some(PankseppEmotion::Seeking));
    }

    #[test]
    fn test_classify_file() {
        let classifier = DhatuClassifier::new();
        
        let path = Path::new("/home/user/project/src/main.rs");
        let intensity = classifier.classify_file(path);
        
        assert!(intensity.seeking > 0.0);
    }
}
EOFCLASSIFIER

echo "✅ classifier.rs created"

echo "Creating profile.rs..."
cat > crates/panini-core/src/dhatu/profile.rs << 'EOFPROFILE'
//! Emotional Profile System
//!
//! Track emotional characteristics of files, directories, and projects

use super::emotion::{EmotionalIntensity, PankseppEmotion};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use chrono::{DateTime, Utc};

/// Emotional profile for a file or directory
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotionalProfile {
    /// File or directory path
    pub path: String,
    
    /// Content hash (SHA-256)
    pub content_hash: Option<String>,
    
    /// Emotional intensity scores
    pub intensity: EmotionalIntensity,
    
    /// Dominant emotion
    pub dominant_emotion: Option<PankseppEmotion>,
    
    /// Classification confidence (0.0 - 1.0)
    pub confidence: f64,
    
    /// Manual tags added by user
    pub manual_tags: Vec<String>,
    
    /// Dhātu roots associated
    pub dhatu_roots: Vec<String>,
    
    /// Timestamp of classification
    pub classified_at: DateTime<Utc>,
    
    /// Optional metadata
    #[serde(default)]
    pub metadata: HashMap<String, String>,
}

impl EmotionalProfile {
    pub fn new(path: String, intensity: EmotionalIntensity) -> Self {
        let dominant_emotion = intensity.dominant();
        let confidence = if let Some(emotion) = dominant_emotion {
            intensity.get(emotion)
        } else {
            0.0
        };
        
        Self {
            path,
            content_hash: None,
            intensity,
            dominant_emotion,
            confidence,
            manual_tags: Vec::new(),
            dhatu_roots: Vec::new(),
            classified_at: Utc::now(),
            metadata: HashMap::new(),
        }
    }
    
    pub fn with_hash(mut self, hash: String) -> Self {
        self.content_hash = Some(hash);
        self
    }
    
    pub fn with_tags(mut self, tags: Vec<String>) -> Self {
        self.manual_tags = tags;
        self
    }
    
    pub fn with_roots(mut self, roots: Vec<String>) -> Self {
        self.dhatu_roots = roots;
        self
    }
    
    pub fn add_tag(&mut self, tag: String) {
        if !self.manual_tags.contains(&tag) {
            self.manual_tags.push(tag);
        }
    }
    
    pub fn add_root(&mut self, root: String) {
        if !self.dhatu_roots.contains(&root) {
            self.dhatu_roots.push(root);
        }
    }
}

/// Resonance between two emotional profiles
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EmotionalResonance {
    /// Path A
    pub path_a: String,
    
    /// Path B
    pub path_b: String,
    
    /// Resonance score (0.0 - 1.0)
    pub score: f64,
    
    /// Shared emotions
    pub shared_emotions: Vec<PankseppEmotion>,
    
    /// Resonance type
    pub resonance_type: ResonanceType,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ResonanceType {
    /// Both have similar dominant emotion
    Harmonic,
    
    /// Complementary emotions (e.g., SEEKING + CARE)
    Complementary,
    
    /// Opposing emotions (e.g., RAGE + CARE)
    Dissonant,
}

impl EmotionalResonance {
    /// Calculate resonance between two profiles
    pub fn calculate(a: &EmotionalProfile, b: &EmotionalProfile) -> Self {
        let mut score = 0.0;
        let mut shared_emotions = Vec::new();
        
        // Calculate cosine similarity of intensity vectors
        for emotion in PankseppEmotion::all() {
            let a_val = a.intensity.get(emotion);
            let b_val = b.intensity.get(emotion);
            
            if a_val > 0.0 && b_val > 0.0 {
                shared_emotions.push(emotion);
            }
            
            score += a_val * b_val;
        }
        
        // Normalize
        let a_norm = a.intensity.arousal();
        let b_norm = b.intensity.arousal();
        if a_norm > 0.0 && b_norm > 0.0 {
            score /= (a_norm * b_norm).sqrt();
        }
        
        // Determine resonance type
        let resonance_type = if a.dominant_emotion == b.dominant_emotion {
            ResonanceType::Harmonic
        } else if score > 0.5 {
            ResonanceType::Complementary
        } else {
            ResonanceType::Dissonant
        };
        
        Self {
            path_a: a.path.clone(),
            path_b: b.path.clone(),
            score: score.clamp(0.0, 1.0),
            shared_emotions,
            resonance_type,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_emotional_profile() {
        let mut intensity = EmotionalIntensity::new();
        intensity.set(PankseppEmotion::Seeking, 0.8);
        
        let profile = EmotionalProfile::new("/test/file.rs".to_string(), intensity);
        
        assert_eq!(profile.dominant_emotion, Some(PankseppEmotion::Seeking));
        assert_eq!(profile.confidence, 0.8);
    }

    #[test]
    fn test_resonance() {
        let mut intensity_a = EmotionalIntensity::new();
        intensity_a.set(PankseppEmotion::Seeking, 0.8);
        let profile_a = EmotionalProfile::new("/a".to_string(), intensity_a);
        
        let mut intensity_b = EmotionalIntensity::new();
        intensity_b.set(PankseppEmotion::Seeking, 0.7);
        let profile_b = EmotionalProfile::new("/b".to_string(), intensity_b);
        
        let resonance = EmotionalResonance::calculate(&profile_a, &profile_b);
        
        assert_eq!(resonance.resonance_type, ResonanceType::Harmonic);
        assert!(resonance.score > 0.0);
    }
}
EOFPROFILE

echo "✅ profile.rs created"

echo "Creating mod.rs..."
cat > crates/panini-core/src/dhatu/mod.rs << 'EOFMOD'
//! Dhātu: Emotional Classification System
//!
//! Named after Sanskrit धातु (dhātu) - "root" or "element"
//! Combines Panksepp's affective neuroscience with Sanskrit linguistic roots
//! 
//! ## Features
//! - Seven primary emotion classification (Panksepp model)
//! - Sanskrit verbal root (dhātu) association
//! - Automatic file/content emotional profiling
//! - Emotional resonance calculation
//! - Temporal emotional analysis

pub mod emotion;
pub mod root;
pub mod classifier;
pub mod profile;

pub use emotion::{PankseppEmotion, EmotionalIntensity};
pub use root::{DhatuRoot, DhatuCatalog};
pub use classifier::DhatuClassifier;
pub use profile::{EmotionalProfile, EmotionalResonance, ResonanceType};
EOFMOD

echo "✅ mod.rs created"

echo "Updating panini-core lib.rs..."
# Add dhatu module to lib.rs
if ! grep -q "pub mod dhatu" /home/stephane/GitHub/Panini-FS/crates/panini-core/src/lib.rs; then
    echo "pub mod dhatu;" >> /home/stephane/GitHub/Panini-FS/crates/panini-core/src/lib.rs
    echo "✅ Added dhatu to lib.rs"
else
    echo "⚠️  dhatu already in lib.rs"
fi

echo ""
echo "🎉 All Dhātu files generated successfully!"
