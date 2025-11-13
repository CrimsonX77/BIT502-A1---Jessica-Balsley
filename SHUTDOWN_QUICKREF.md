# 🌙 Graceful Shutdown - Quick Reference

## What It Does
Ensures all timers, threads, dialogs, and resources are properly cleaned up when closing the application. No crashes, no hangs, no orphaned processes.

## How To Use

### As a User
1. Click **"Leave Archive"** in the quest menu
2. Confirm in the dialog
3. Wait ~3-4 seconds for graceful cleanup
4. Application closes cleanly

### As a Developer

#### Adding Tracked Resources

**Timer:**
```python
# Create
timer = QTimer()
timer.timeout.connect(self.callback)
timer.start(interval)

# Track
self.active_timers.append(timer)

# Cleanup happens automatically on shutdown
```

**Dialog:**
```python
# Create
dialog = MyDialog(self)

# Track
self.active_dialogs.append(dialog)

# Show
result = dialog.exec()

# Untrack
self.active_dialogs.remove(dialog)

# Cleanup happens automatically if still open during shutdown
```

**Worker Thread:**
```python
# Create
worker = MyWorker()

# Track
self.active_workers.append(worker)

# Start
worker.start()

# Auto-untrack when done
worker.finished.connect(lambda: self.active_workers.remove(worker))

# Cleanup happens automatically if still running during shutdown
```

## Shutdown Flow

```
User Action
    ↓
Confirmation Dialog
    ↓
cleanup_resources()
    ├→ cleanup_timers()      [Stop all QTimers]
    ├→ cleanup_dialogs()     [Close all QDialogs]
    └→ cleanup_workers()     [Terminate all QThreads]
    ↓
finalize_shutdown()
    ↓
session_ended.emit()
    ↓
Launcher Cascade
    ├→ Close Sanctum (1.5s)
    ├→ Close Obelisk (0.5s)
    └→ Finalize (1.0s)
    ↓
QApplication.quit()
```

## Timing

| Stage | Component | Delay | Total |
|-------|-----------|-------|-------|
| Cleanup | Sanctum | 500ms | 0.5s |
| Finalize | Sanctum | 1000ms | 1.5s |
| Close Sanctum | Launcher | 1500ms | 3.0s |
| Close Obelisk | Launcher | 500ms | 3.5s |
| Quit | Launcher | 500ms | 4.0s |

**Total Shutdown Time: ~3.5-4 seconds**

## Verification

### Check Cleanup is Working
```python
# Before shutdown - should see timers active
print(f"Active timers: {len(self.active_timers)}")
print(f"Active dialogs: {len(self.active_dialogs)}")
print(f"Active workers: {len(self.active_workers)}")

# After cleanup_resources() - should be 0
# All lists cleared, all resources stopped
```

### Console Output
```
🔄 Initiating cascading shutdown...
  → Closing Archive Sanctum...
  ✅ Archive Sanctum closed
  → Closing Obelisk Customs...
  ✅ Obelisk Customs closed
✨ Shutdown complete. The Crimson Collective awaits your return...
```

## Common Issues

### Shutdown Hangs
**Problem**: Application doesn't close  
**Solution**: Check for blocking operations in timer callbacks or worker threads

### Incomplete Cleanup
**Problem**: Resources still active after cleanup  
**Solution**: Verify all resources added to tracking lists

### Crash on Close
**Problem**: Application crashes during shutdown  
**Solution**: Check for null pointer access or signals to deleted objects

## Testing

```bash
# Launch
python collective_launcher.py

# Use the app
# Click "Leave Archive"
# Confirm logout
# Watch console for cleanup messages
# Verify clean exit (no errors)
```

## Files Modified

- `archive_sanctum.py` - Added shutdown system
- `obelisk_customs.py` - Added shutdown system  
- `collective_launcher.py` - Added cascading orchestration
- `GRACEFUL_SHUTDOWN.md` - Complete documentation
- `INTEGRATION_GUIDE.md` - Integration details

## Quick Stats

- **Archive Sanctum**: 1,153 lines (added ~150 lines for shutdown)
- **Obelisk Customs**: 570 lines (added ~50 lines for shutdown)
- **Collective Launcher**: 160 lines (new file)
- **Total Cleanup Code**: ~200 lines across all files

---

**Result**: No more jarring crashes. Clean, professional shutdown. The Crimson Collective shuts down as elegantly as it opens. 🔮
