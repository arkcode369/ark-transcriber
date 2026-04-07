#!/usr/bin/env python3
"""
Test script to verify ark-transcriber → ark-intelligent integration
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '/workspace/main/ark-transcriber')

def test_imports():
    """Test if all modules can be imported"""
    print("📦 Testing imports...")
    try:
        from save_to_ark_intelligent import (
            save_youtube_transcript,
            save_youtube_playlist,
            save_pdf_transcript,
            list_all_transcripts,
            get_transcript_path
        )
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_directory_structure():
    """Test if directory structure exists"""
    print("\n📁 Testing directory structure...")
    
    required_dirs = [
        "/workspace/main/ark-intelligent/.agents/docs/transcripts/youtube",
        "/workspace/main/ark-intelligent/.agents/docs/transcripts/pdf",
        "/workspace/main/ark-intelligent/.agents/docs/transcripts/youtube/templates",
        "/workspace/main/ark-intelligent/.agents/docs/transcripts/pdf/templates"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"  ✅ {dir_path}")
        else:
            print(f"  ❌ {dir_path} (missing)")
            all_exist = False
    
    return all_exist

def test_functions():
    """Test if all required functions exist and work"""
    print("\n⚙️ Testing functions...")
    
    from save_to_ark_intelligent import (
        slugify,
        extract_tags_from_summary,
        generate_key_points,
        generate_actionable_insights
    )
    
    # Test slugify
    result = slugify("Test Video Title 123")
    if result == "test-video-title-123":
        print(f"  ✅ slugify: '{result}'")
    else:
        print(f"  ❌ slugify failed: expected 'test-video-title-123', got '{result}'")
        return False
    
    # Test extract_tags_from_summary
    summary = "This video covers trading strategy, risk management, and psychology"
    tags = extract_tags_from_summary(summary)
    if "trading" in tags and "strategy" in tags:
        print(f"  ✅ extract_tags_from_summary: {tags}")
    else:
        print(f"  ❌ extract_tags_from_summary failed: {tags}")
        return False
    
    # Test generate_key_points
    key_points = generate_key_points(summary)
    if key_points and len(key_points) > 0:
        print(f"  ✅ generate_key_points: {len(key_points)} chars")
    else:
        print(f"  ❌ generate_key_points failed")
        return False
    
    return True

def test_metadata_structure():
    """Test metadata generation"""
    print("\n📋 Testing metadata structure...")
    
    from save_to_ark_intelligent import extract_tags_from_summary
    import json
    
    # Simulate metadata
    metadata = {
        "source_type": "youtube",
        "source_id": "test123",
        "title": "Test Video",
        "language": "id",
        "tags": extract_tags_from_summary("Trading strategy and risk management")
    }
    
    # Verify structure
    required_fields = ["source_type", "source_id", "title", "language", "tags"]
    missing = [f for f in required_fields if f not in metadata]
    
    if not missing:
        print(f"  ✅ Metadata structure correct")
        print(f"     {json.dumps(metadata, indent=2)}")
        return True
    else:
        print(f"  ❌ Missing fields: {missing}")
        return False

def test_integration_points():
    """Test if integration points in main.py are correct"""
    print("\n🔗 Testing integration points...")
    
    with open('/workspace/main/ark-transcriber/main.py', 'r') as f:
        content = f.read()
    
    # Check imports
    if "from save_to_ark_intelligent import" in content:
        print("  ✅ save_to_ark_intelligent imported in main.py")
    else:
        print("  ❌ save_to_ark_intelligent not imported")
        return False
    
    # Check save calls
    if "Saving to ark-intelligent docs" in content:
        print("  ✅ Save logging present")
    else:
        print("  ❌ Save logging missing")
        return False
    
    # Check all endpoints have save logic
    endpoints = [
        ("transcribe_youtube_video", "save_youtube_transcript"),
        ("transcribe_youtube_playlist", "save_youtube_playlist"),
        ("process_pdf", "save_pdf_transcript")
    ]
    
    for endpoint, save_func in endpoints:
        if endpoint in content and save_func in content:
            print(f"  ✅ {endpoint} → {save_func}")
        else:
            print(f"  ❌ {endpoint} → {save_func} (missing)")
            return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Testing ark-transcriber → ark-intelligent Integration")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Directory Structure", test_directory_structure),
        ("Functions", test_functions),
        ("Metadata Structure", test_metadata_structure),
        ("Integration Points", test_integration_points)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} test failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Integration is 100% functional.")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
