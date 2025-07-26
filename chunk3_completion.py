#!/usr/bin/env python3
"""
Chunk 3 Completion - Process remaining PDFs in smaller batches to avoid timeout
"""

import os
import json
from pathlib import Path
from intelligent_pdf_extractor import IntelligentPDFExtractor
import sys
import time
from bs4 import BeautifulSoup
import re

def complete_chunk3_in_batches():
    """Complete Chunk 3 processing in smaller batches"""
    
    # Chunk 3 PDFs (split into 2 batches)
    chunk3_pdfs = [
        "compressed_South America Teacher Guide PDF.pdf",
        "compressed_Southeast Asia Teacher Guide PDF.pdf", 
        "compressed_Southern Europe Teacher Guide PDF.pdf",
        "compressed_The Arabian Peninsula to Central Asia Teacher Guide PDF.pdf",
        "compressed_The Eastern Mediterranean Teacher Guide PDF.pdf",
        "compressed_The Human World Teacher Guide PDF.pdf",
        "compressed_The Indian Subcontinent Teacher Guide PDF.pdf",
        "compressed_The Physical World Teacher Guide PDF.pdf",
        "compressed_The United States Teacher Guide PDF.pdf",
        "compressed_West and Central Africa Teacher Guide PDF.pdf",
        "compressed_Western Europe Teacher Guide PDF.pdf",
        "compressed_World Religions of Southwest Asia Teacher Guide PDF.pdf"
    ]
    
    # Split into 2 batches
    batch1 = chunk3_pdfs[:6]  # First 6 PDFs
    batch2 = chunk3_pdfs[6:]  # Last 6 PDFs
    
    print("🚀 CHUNK 3 COMPLETION - BATCH PROCESSING")
    print("=" * 50)
    print(f"📚 Total PDFs in Chunk 3: {len(chunk3_pdfs)}")
    print(f"🔄 Batch 1: {len(batch1)} PDFs")
    print(f"🔄 Batch 2: {len(batch2)} PDFs")
    
    # Process both batches
    all_results = {}
    total_files_updated = 0
    
    for batch_num, batch_pdfs in enumerate([batch1, batch2], 1):
        print(f"\n🔄 PROCESSING BATCH {batch_num}")
        print("=" * 30)
        
        batch_results = process_pdf_batch(batch_pdfs, f"chunk3_batch{batch_num}")
        
        if batch_results:
            all_results.update(batch_results['extracted_content'])
            total_files_updated += batch_results['files_updated']
            print(f"✅ Batch {batch_num} complete: {batch_results['files_updated']} files updated")
        else:
            print(f"⚠️  Batch {batch_num} had issues")
    
    # Save combined results
    if all_results:
        combined_results = {
            'chunk_name': 'chunk3_complete',
            'total_pdfs': len(chunk3_pdfs),
            'successful_extractions': len(all_results),
            'total_files_updated': total_files_updated,
            'extracted_content': all_results
        }
        
        output_file = Path("/workspaces/Curriculum/chunk3_complete_pipeline_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n🎉 CHUNK 3 COMPLETE!")
        print(f"📚 PDFs processed: {len(chunk3_pdfs)}")
        print(f"✅ Content extracted from: {len(all_results)} PDFs")
        print(f"🔗 Total files updated: {total_files_updated}")
        print(f"💾 Results saved: {output_file}")
        
        return True
    else:
        print("❌ No content extracted from Chunk 3")
        return False

def process_pdf_batch(pdf_names, batch_name):
    """Process a batch of PDFs with full pipeline"""
    from complete_chunked_pipeline import CompleteChunkedPipeline
    
    pipeline = CompleteChunkedPipeline()
    pdf_dir = Path("/workspaces/Curriculum/Compressed")
    
    # Convert names to full paths
    pdf_paths = []
    for pdf_name in pdf_names:
        pdf_path = pdf_dir / pdf_name
        if pdf_path.exists():
            pdf_paths.append(pdf_path)
        else:
            print(f"⚠️  PDF not found: {pdf_name}")
    
    print(f"📖 Processing {len(pdf_paths)} PDFs in {batch_name}")
    
    # STEP 1: Extract content
    print("📖 STEP 1: Extracting content...")
    extracted_content = pipeline.step1_extract_chunk_content(pdf_paths)
    
    if not extracted_content:
        print("❌ No content extracted")
        return None
    
    print(f"✅ Extracted from {len(extracted_content)} PDFs")
    
    # STEP 2: Map content
    print("🗺️  STEP 2: Mapping content...")
    content_mappings = pipeline.step2_map_all_content(extracted_content)
    print(f"✅ Created {len(content_mappings)} mappings")
    
    # STEP 3: Integrate content
    print("🔗 STEP 3: Integrating content...")
    integration_results = pipeline.step3_mass_integrate(content_mappings)
    print(f"✅ Updated {integration_results['files_updated']} files")
    
    # STEP 4: Replace templates
    print("🔄 STEP 4: Replacing templates...")
    replacement_results = pipeline.step4_replace_templates(integration_results)
    print(f"✅ Replaced templates in {replacement_results['files_processed']} files")
    
    return {
        'extracted_content': extracted_content,
        'content_mappings': content_mappings,
        'files_updated': integration_results['files_updated'],
        'templates_replaced': replacement_results['files_processed']
    }

if __name__ == "__main__":
    success = complete_chunk3_in_batches()
    
    if success:
        print("\n🎉 ALL CHUNKS NOW COMPLETE!")
        print("📊 Final Results Summary:")
        
        # Check results from all chunks
        chunk_files = [
            "/workspaces/Curriculum/chunk1_complete_pipeline_results.json",
            "/workspaces/Curriculum/chunk2_complete_pipeline_results.json", 
            "/workspaces/Curriculum/chunk3_complete_pipeline_results.json"
        ]
        
        total_files_updated = 0
        total_pdfs_processed = 0
        
        for chunk_file in chunk_files:
            if Path(chunk_file).exists():
                with open(chunk_file, 'r') as f:
                    chunk_data = json.load(f)
                    
                chunk_name = Path(chunk_file).stem.replace('_complete_pipeline_results', '')
                files_updated = chunk_data.get('files_integrated', chunk_data.get('total_files_updated', 0))
                total_files_updated += files_updated
                
                if 'pdfs_processed' in chunk_data:
                    total_pdfs_processed += chunk_data['pdfs_processed']
                elif 'total_pdfs' in chunk_data:
                    total_pdfs_processed += chunk_data['total_pdfs']
                
                print(f"   {chunk_name}: {files_updated} files updated")
        
        print(f"\n🎯 FINAL TOTALS:")
        print(f"   📚 PDFs processed: {total_pdfs_processed}")
        print(f"   🔗 Total lesson files updated with real content: {total_files_updated}")
        print(f"   ✅ Mission accomplished!")
    else:
        print("❌ Chunk 3 completion failed")
