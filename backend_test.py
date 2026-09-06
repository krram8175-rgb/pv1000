#!/usr/bin/env python3
"""
Backend API Testing Script for Units & Measurements Q5 and Q8 Image/Data Fix
Tests the NEET Physics chapter bank endpoint and image serving
"""

import requests
import sys
from typing import Dict, Any

# Backend URL from frontend/.env
BASE_URL = "https://pv608-core.preview.emergentagent.com/api"

def test_chapter_bank_structure():
    """
    Test 1: Verify chapter bank returns HTTP 200, total_questions == 55, 
    and sections[0] contains 55 questions
    """
    print("\n" + "="*80)
    print("TEST 1: Chapter Bank Structure")
    print("="*80)
    
    url = f"{BASE_URL}/chapter-bank/neet-physics-units-and-measurements"
    print(f"GET {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected HTTP 200, got {response.status_code}")
            return False
        
        data = response.json()
        total_questions = data.get("total_questions", 0)
        print(f"Total Questions: {total_questions}")
        
        if total_questions != 55:
            print(f"❌ FAILED: Expected total_questions == 55, got {total_questions}")
            return False
        
        sections = data.get("sections", [])
        if not sections:
            print("❌ FAILED: No sections found in response")
            return False
        
        section_0_questions = len(sections[0].get("questions", []))
        print(f"Section 0 Question Count: {section_0_questions}")
        
        if section_0_questions != 55:
            print(f"❌ FAILED: Expected sections[0] to have 55 questions, got {section_0_questions}")
            return False
        
        print("✅ PASSED: Chapter bank structure is correct")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception occurred - {str(e)}")
        return False


def test_question_5_images():
    """
    Test 2: Verify Question 5 has correct image filenames
    """
    print("\n" + "="*80)
    print("TEST 2: Question 5 Image Filenames")
    print("="*80)
    
    url = f"{BASE_URL}/chapter-bank/neet-physics-units-and-measurements"
    print(f"GET {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"❌ FAILED: Could not fetch chapter bank (HTTP {response.status_code})")
            return False
        
        data = response.json()
        sections = data.get("sections", [])
        
        # Find question 5
        question_5 = None
        for section in sections:
            for q in section.get("questions", []):
                if q.get("question_no") == 5:
                    question_5 = q
                    break
            if question_5:
                break
        
        if not question_5:
            print("❌ FAILED: Question 5 not found in chapter bank")
            return False
        
        print(f"Found Question 5: question_no={question_5.get('question_no')}")
        
        # Check question_image
        expected_question_image = "uam-fullpaper-q5.png"
        actual_question_image = question_5.get("question_image", "")
        print(f"  question_image: {actual_question_image}")
        
        if actual_question_image != expected_question_image:
            print(f"❌ FAILED: Expected question_image='{expected_question_image}', got '{actual_question_image}'")
            return False
        
        # Check solution_image
        expected_solution_image = "uam-fullpaper-q5-sol-v2.png"
        actual_solution_image = question_5.get("solution_image", "")
        print(f"  solution_image: {actual_solution_image}")
        
        if actual_solution_image != expected_solution_image:
            print(f"❌ FAILED: Expected solution_image='{expected_solution_image}', got '{actual_solution_image}'")
            return False
        
        # Check option_images
        expected_option_images = {
            "a": "uam-fullpaper-q5-a.png",
            "b": "uam-fullpaper-q5-b.png",
            "c": "uam-fullpaper-q5-c.png",
            "d": "uam-fullpaper-q5-d.png"
        }
        actual_option_images = question_5.get("option_images", {})
        print(f"  option_images: {actual_option_images}")
        
        for key, expected_filename in expected_option_images.items():
            actual_filename = actual_option_images.get(key, "")
            if actual_filename != expected_filename:
                print(f"❌ FAILED: Expected option_images[{key}]='{expected_filename}', got '{actual_filename}'")
                return False
        
        print("✅ PASSED: Question 5 has correct image filenames")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception occurred - {str(e)}")
        return False


def test_question_8_images():
    """
    Test 3: Verify Question 8 has correct image filenames (reuses Q5's option images)
    """
    print("\n" + "="*80)
    print("TEST 3: Question 8 Image Filenames")
    print("="*80)
    
    url = f"{BASE_URL}/chapter-bank/neet-physics-units-and-measurements"
    print(f"GET {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"❌ FAILED: Could not fetch chapter bank (HTTP {response.status_code})")
            return False
        
        data = response.json()
        sections = data.get("sections", [])
        
        # Find question 8
        question_8 = None
        for section in sections:
            for q in section.get("questions", []):
                if q.get("question_no") == 8:
                    question_8 = q
                    break
            if question_8:
                break
        
        if not question_8:
            print("❌ FAILED: Question 8 not found in chapter bank")
            return False
        
        print(f"Found Question 8: question_no={question_8.get('question_no')}")
        
        # Check question_image
        expected_question_image = "uam-fullpaper-q8.png"
        actual_question_image = question_8.get("question_image", "")
        print(f"  question_image: {actual_question_image}")
        
        if actual_question_image != expected_question_image:
            print(f"❌ FAILED: Expected question_image='{expected_question_image}', got '{actual_question_image}'")
            return False
        
        # Check solution_image
        expected_solution_image = "uam-fullpaper-q8-sol-v2.png"
        actual_solution_image = question_8.get("solution_image", "")
        print(f"  solution_image: {actual_solution_image}")
        
        if actual_solution_image != expected_solution_image:
            print(f"❌ FAILED: Expected solution_image='{expected_solution_image}', got '{actual_solution_image}'")
            return False
        
        # Check option_images (Q8 reuses Q5's option images)
        expected_option_images = {
            "a": "uam-fullpaper-q5-a.png",
            "b": "uam-fullpaper-q5-b.png",
            "c": "uam-fullpaper-q5-c.png",
            "d": "uam-fullpaper-q5-d.png"
        }
        actual_option_images = question_8.get("option_images", {})
        print(f"  option_images: {actual_option_images}")
        
        for key, expected_filename in expected_option_images.items():
            actual_filename = actual_option_images.get(key, "")
            if actual_filename != expected_filename:
                print(f"❌ FAILED: Expected option_images[{key}]='{expected_filename}', got '{actual_filename}'")
                return False
        
        print("✅ PASSED: Question 8 has correct image filenames (reuses Q5's option images)")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception occurred - {str(e)}")
        return False


def test_image_serving():
    """
    Test 4: Verify all image files serve correctly via GET /api/chapter-image/<filename>
    """
    print("\n" + "="*80)
    print("TEST 4: Image File Serving")
    print("="*80)
    
    image_files = [
        "uam-fullpaper-q5-sol-v2.png",
        "uam-fullpaper-q8-sol-v2.png",
        "uam-fullpaper-q5-a.png",
        "uam-fullpaper-q5-b.png",
        "uam-fullpaper-q5-c.png",
        "uam-fullpaper-q5-d.png",
        "uam-fullpaper-q8.png"
    ]
    
    all_passed = True
    
    for filename in image_files:
        url = f"{BASE_URL}/chapter-image/{filename}"
        print(f"\nGET {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"  Status Code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"  ❌ FAILED: Expected HTTP 200, got {response.status_code}")
                all_passed = False
                continue
            
            content_type = response.headers.get("Content-Type", "")
            print(f"  Content-Type: {content_type}")
            
            if content_type != "image/png":
                print(f"  ❌ FAILED: Expected Content-Type 'image/png', got '{content_type}'")
                all_passed = False
                continue
            
            content_length = len(response.content)
            print(f"  Content-Length: {content_length} bytes")
            
            if content_length == 0:
                print(f"  ❌ FAILED: Image file is empty")
                all_passed = False
                continue
            
            print(f"  ✅ PASSED: {filename} serves correctly")
            
        except Exception as e:
            print(f"  ❌ FAILED: Exception occurred - {str(e)}")
            all_passed = False
    
    if all_passed:
        print("\n✅ PASSED: All image files serve correctly")
    else:
        print("\n❌ FAILED: Some image files failed to serve")
    
    return all_passed


def main():
    """Run all tests and report results"""
    print("="*80)
    print("NEET Physics Units & Measurements Q5/Q8 Image Fix Verification")
    print("="*80)
    print(f"Backend URL: {BASE_URL}")
    
    results = {
        "Chapter Bank Structure": test_chapter_bank_structure(),
        "Question 5 Images": test_question_5_images(),
        "Question 8 Images": test_question_8_images(),
        "Image File Serving": test_image_serving()
    }
    
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_tests = len(results)
    passed_tests = sum(1 for p in results.values() if p)
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if all(results.values()):
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
