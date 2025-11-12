#!/bin/bash
# Add DhatuState to AppState

cd /home/stephane/GitHub/Panini-FS

FILE="crates/panini-api/src/state.rs"
cp "$FILE" "$FILE.backup"

# Replace the entire file with the new version
cat > "$FILE" << 'EOFSTATE'
//! Application state shared across handlers

use crate::dhatu_handlers::DhatuState;
use panini_core::storage::{
    backends::localfs::LocalFsBackend,
    cas::ContentAddressedStorage,
    immutable::TemporalIndex,
};
use std::sync::{Arc, RwLock};

/// Shared application state
#[derive(Clone)]
pub struct AppState {
    /// Temporal index for time-travel queries
    pub temporal_index: Arc<RwLock<TemporalIndex>>,
    
    /// Content-addressed storage
    pub cas: Arc<ContentAddressedStorage<LocalFsBackend>>,
    
    /// Dhātu emotional classification system
    pub dhatu: Arc<DhatuState>,
}

impl AppState {
    /// Create new application state
    pub fn new(
        temporal_index: Arc<RwLock<TemporalIndex>>,
        cas: Arc<ContentAddressedStorage<LocalFsBackend>>,
    ) -> Self {
        Self {
            temporal_index,
            cas,
            dhatu: DhatuState::new(),
        }
    }
}
EOFSTATE

echo "✅ DhatuState added to AppState"
cat "$FILE"
