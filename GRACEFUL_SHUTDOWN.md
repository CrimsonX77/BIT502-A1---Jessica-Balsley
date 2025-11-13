# 🔄 GRACEFUL SHUTDOWN SYSTEM

## Overview
The Crimson Collective authentication system implements comprehensive graceful shutdown with cascading resource cleanup across all GUI layers.

## Architecture

### Multi-Layer System
```
┌─────────────────────────┐
│  Collective Launcher    │ ← Master orchestrator
│  (collective_launcher)  │
└──────────┬──────────────┘
           │
    ┌──────┴────────┐
    ▼               ▼
┌────────┐     ┌─────────┐
│Obelisk │────→│ Sanctum │
│Customs │◄────│ Archive │
└────────┘     └─────────┘
 Layer 1        Layer 2
```

### Signal Flow
```
Sanctum Logout Button
       │
       ▼
session_ended Signal
       │
       ▼
Launcher.on_sanctum_logout()
       │
       ▼
Cascading Shutdown:
  1. Close Sanctum (1.5s delay)
  2. Close Obelisk (0.5s delay)
  3. Cleanup Resources (1.0s delay)
  4. Exit Application (0.5s delay)
```

---

## Component Details

### 1. Archive Sanctum (archive_sanctum.py)

#### Resource Tracking
```python
self.is_shutting_down = False
self.active_timers = []      # QTimer instances
self.active_dialogs = []     # QDialog instances
```

#### Cleanup Methods

**cleanup_timers()**
- Stops all active QTimer instances
- Clears timer list
- Prevents residual timer callbacks

**cleanup_dialogs()**
- Closes all open QDialog windows
- Removes from tracking list
- Ensures no orphaned modals

**cleanup_resources()**
- Master cleanup orchestrator
- Updates status message
- Calls timer cleanup
- Calls dialog cleanup
- Schedules finalize_shutdown() after 500ms

**finalize_shutdown()**
- Shows farewell message
- Closes window after 1000ms delay
- Emits `session_ended` signal

**logout_and_close()**
- Shows confirmation dialog
- "Stay in Archive" or "Leave Archive" options
- On confirm: Triggers cleanup cascade
- On cancel: Resume session

#### Tracked Resources

**Active Timers**:
- Status rotation timer (5-second cycle)
- Any animation timers
- Periodic update timers

**Active Dialogs**:
- Tier ascension dialog
- Achievement galleries
- Settings panels
- Any modal windows

#### Close Event Override
```python
def closeEvent(self, event):
    if not self.is_shutting_down:
        event.ignore()  # Block direct close
        self.logout_and_close()  # Show confirmation
    else:
        event.accept()  # Allow close during cleanup
```

---

### 2. Obelisk Customs (obelisk_customs.py)

#### Resource Tracking
```python
self.is_shutting_down = False
self.active_workers = []     # QThread instances
self.active_dialogs = []     # QDialog instances
```

#### Cleanup Methods

**cleanup_workers()**
- Terminates background verification threads
- Waits up to 1 second per thread
- Clears worker list
- Prevents hanging threads

**cleanup_dialogs()**
- Same as Sanctum implementation

**cleanup_resources()**
- Updates log and status
- Calls worker cleanup
- Calls dialog cleanup
- Closes window after 500ms

#### Tracked Resources

**Active Workers**:
- CardVerificationWorker threads
- Background processing tasks
- Any async operations

**Active Dialogs**:
- Validation result dialogs
- Error/warning modals

#### Close Event Override
```python
def closeEvent(self, event):
    if not self.is_shutting_down:
        self.cleanup_resources()
        event.ignore()
        QTimer.singleShot(600, self.close)
    else:
        event.accept()
```

---

### 3. Collective Launcher (collective_launcher.py)

#### Master Orchestrator
Manages the complete lifecycle of both GUIs with proper shutdown sequencing.

#### Shutdown Stages

**Stage 1: Initiate (0ms)**
```python
def initiate_shutdown(self):
    self.is_shutting_down = True
    # Close Sanctum first
    self.sanctum.cleanup_resources()
```

**Stage 2: Close Sanctum (1500ms delay)**
```python
def _close_sanctum(self):
    self.sanctum.close()
    self.sanctum = None
    # Schedule Obelisk close
```

**Stage 3: Close Obelisk (500ms delay)**
```python
def _close_obelisk(self):
    self.obelisk.cleanup_resources()
    # Schedule finalize
```

**Stage 4: Finalize (1000ms delay)**
```python
def _finalize_shutdown(self):
    self.obelisk.close()
    self.obelisk = None
    QApplication.quit()
```

**Total Shutdown Time**: ~3.5 seconds

---

## Usage Patterns

### For Users

1. **Normal Logout**:
   - Click "Leave Archive" quest item
   - Or click X on window
   - Confirm in dialog
   - Wait for graceful cleanup (3-4 seconds)

2. **Emergency Close**:
   - Press Alt+F4 or close from taskbar
   - System still triggers cleanup
   - May take slightly longer

### For Developers

#### Adding New Timers
```python
# Create timer
self.my_timer = QTimer()
self.my_timer.timeout.connect(self.my_callback)
self.my_timer.start(1000)

# Track it!
self.active_timers.append(self.my_timer)
```

#### Adding New Dialogs
```python
# Create dialog
dialog = MyCustomDialog(self)

# Track it!
self.active_dialogs.append(dialog)

# Show dialog
result = dialog.exec()

# Untrack after close
self.active_dialogs.remove(dialog)
```

#### Adding New Workers
```python
# Create worker
worker = MyBackgroundWorker()
self.active_workers.append(worker)

# Start worker
worker.start()

# When done
worker.finished.connect(lambda: self.active_workers.remove(worker))
```

---

## Timing Configuration

### Archive Sanctum
- Logout confirmation: Immediate
- Cleanup initiation: 500ms
- Finalize close: 1000ms
- **Total**: ~1.5 seconds

### Obelisk Customs
- Cleanup initiation: Immediate
- Worker termination: 1000ms per worker
- Final close: 600ms
- **Total**: ~1.6 seconds

### Collective Launcher
- Sanctum → Obelisk: 1500ms delay
- Obelisk → Finalize: 500ms delay
- Finalize → Quit: 1000ms delay
- **Total**: ~3.5 seconds full cascade

---

## Error Handling

### Thread Cleanup Timeout
If a worker thread doesn't terminate within 1 second:
```python
worker.terminate()
worker.wait(1000)  # Force terminate after timeout
```

### Dialog Close Failure
If dialog.close() fails, continues cleanup:
```python
for dialog in self.active_dialogs[:]:
    try:
        dialog.close()
    except:
        pass  # Continue cleaning up others
```

### Timer Stop Failure
Checks if timer is active before stopping:
```python
if timer and timer.isActive():
    timer.stop()
```

---

## Signal Chain

```
User Action (Click logout)
        ↓
logout_and_close() [Sanctum]
        ↓
Confirmation Dialog
        ↓ (Confirmed)
cleanup_resources() [Sanctum]
        ↓
session_ended Signal EMIT
        ↓
on_sanctum_logout() [Launcher]
        ↓
initiate_shutdown() [Launcher]
        ↓ (1.5s delay)
_close_sanctum() [Launcher]
        ↓ (0.5s delay)
_close_obelisk() [Launcher]
        ↓ (1.0s delay)
_finalize_shutdown() [Launcher]
        ↓ (0.5s delay)
QApplication.quit()
        ↓
Clean Exit
```

---

## Testing Checklist

### Manual Tests
- [ ] Click logout in Sanctum
- [ ] Confirm in dialog
- [ ] Verify status messages update
- [ ] Check console for "Closing..." messages
- [ ] Verify no crashes or hangs
- [ ] Check both windows close
- [ ] Verify clean terminal exit

### Resource Tests
- [ ] Open tier upgrade dialog, then logout
- [ ] Let status timer run, then logout
- [ ] Validate a card (background worker), then logout
- [ ] Cancel logout dialog, verify session continues
- [ ] Direct close window (X button)
- [ ] Force close (Alt+F4)

### Timing Tests
- [ ] Full cascade completes in ~3-4 seconds
- [ ] No jarring freezes
- [ ] Smooth transitions between stages
- [ ] Status messages visible during cleanup

---

## Cryptic Messages

### Archive Sanctum
- During cleanup: "🌙 Closing the Archive Sanctum..."
- Final message: "✨ The Crimson Collective awaits your return..."
- Dialog: "🚪 Are you sure you wish to leave the Archive Sanctum?"

### Obelisk Customs
- During cleanup: "🌙 Shutting down..."
- Log message: "🌙 Closing Obelisk Customs..."

### Launcher Console
- Initiation: "🔄 Initiating cascading shutdown..."
- Sanctum: "→ Closing Archive Sanctum..." / "✅ Archive Sanctum closed"
- Obelisk: "→ Closing Obelisk Customs..." / "✅ Obelisk Customs closed"
- Complete: "✨ Shutdown complete. The Crimson Collective awaits your return..."

---

## Future Enhancements

### Possible Additions
1. **Save Session State**: Preserve open dialogs, timers, positions
2. **Resume Session**: Restore state on next login
3. **Logout Analytics**: Track logout reasons, duration
4. **Force Shutdown Button**: Emergency exit without delays
5. **Shutdown Progress Bar**: Visual feedback during cleanup
6. **Custom Farewell Messages**: Randomized cryptic goodbyes
7. **Sound Effects**: Atmospheric audio during shutdown

### Performance Optimizations
1. **Parallel Cleanup**: Stop timers and workers simultaneously
2. **Async Dialog Close**: Non-blocking dialog cleanup
3. **Configurable Timeouts**: User-adjustable delay times
4. **Skip Delays in Dev Mode**: Faster testing during development

---

## Troubleshooting

### Shutdown Hangs
- Check for infinite loops in timer callbacks
- Verify worker threads terminate
- Look for blocking operations in cleanup

### Incomplete Cleanup
- Verify all resources tracked in lists
- Check for resources created after init
- Ensure cleanup methods called

### Crash on Close
- Check for null pointer access during cleanup
- Verify close event order
- Look for signals emitted to deleted objects

---

## Conclusion

The graceful shutdown system ensures:
✅ No orphaned processes  
✅ No memory leaks  
✅ No jarring crashes  
✅ Smooth user experience  
✅ Clean terminal exit  
✅ Proper resource cleanup  

The Crimson Collective shuts down as elegantly as it opens. 🔮
