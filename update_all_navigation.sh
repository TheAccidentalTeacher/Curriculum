#!/bin/bash

# Script to add navigation to all remaining unit files (6-32)

echo "Adding navigation to all remaining units..."

for i in {6..32}; do
    file="/workspaces/Curriculum/units/unit${i}.html"
    
    if [ -f "$file" ]; then
        echo "Processing unit${i}.html..."
        
        # Determine previous and next unit numbers
        prev=$((i-1))
        next=$((i+1))
        
        # Build navigation elements
        prev_link="<a href=\"unit${prev}.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px;\">⬅ Previous</a>"
        
        if [ $i -eq 32 ]; then
            next_link="<span style=\"color: rgba(255,255,255,0.5); padding: 8px 16px;\">Next ➡</span>"
            footer_next=""
        else
            next_link="<a href=\"unit${next}.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px;\">Next ➡</a>"
            footer_next="<a href=\"unit${next}.html\" style=\"background: #27ae60; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: bold;\">Next: Unit ${next} ➡</a>"
        fi
        
        # Create temporary file for processing
        temp_file=$(mktemp)
        
        # Process the file line by line
        in_header=false
        header_done=false
        main_closed=false
        
        while IFS= read -r line; do
            if [[ "$line" == *"<header>"* ]]; then
                in_header=true
                # Get unit title from the file
                title=$(grep -o '<h1>Unit [^<]*</h1>' "$file" | sed 's/<[^>]*>//g')
                
                # Write new header with navigation
                cat << EOF >> "$temp_file"
    <header>
        <h1>${title}</h1>
        <nav style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <a href="../curriculum-main.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">🏠 Back to Overview</a>
            <div style="display: flex; gap: 15px;">
                <a href="index.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;">📚 All Units</a>
                ${prev_link}
                ${next_link}
            </div>
        </nav>
    </header>
EOF
                continue
            elif [[ "$line" == *"</header>"* ]]; then
                in_header=false
                header_done=true
                continue
            elif [[ "$in_header" == true ]]; then
                # Skip lines inside old header
                continue
            elif [[ "$line" == *"</main>"* ]] && [[ "$main_closed" == false ]]; then
                main_closed=true
                echo "    </main>" >> "$temp_file"
                echo "" >> "$temp_file"
                
                # Add footer navigation
                cat << EOF >> "$temp_file"
    <footer style="text-align: center; margin: 40px 0; padding: 20px; background: rgba(44, 90, 160, 0.1); border-radius: 10px;">
        <div style="display: flex; justify-content: center; gap: 20px; align-items: center;">
            <a href="index.html" style="background: #2c5aa0; color: white; padding: 12px 24px; border-radius: 25px; text-decoration: none; font-weight: bold;">📚 Back to All Units</a>
EOF
                
                if [ $i -ne 32 ]; then
                    echo "            ${footer_next}" >> "$temp_file"
                fi
                
                echo "        </div>" >> "$temp_file"
                echo "    </footer>" >> "$temp_file"
                echo "" >> "$temp_file"
                continue
            else
                echo "$line" >> "$temp_file"
            fi
        done < "$file"
        
        # Replace original file with updated content
        mv "$temp_file" "$file"
        echo "✓ Updated unit${i}.html"
    else
        echo "✗ File unit${i}.html not found"
    fi
done

echo ""
echo "🎉 Navigation update complete for all units!"
echo "All 32 units now have proper Previous/Next navigation!"
