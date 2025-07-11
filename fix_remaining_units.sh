#!/bin/bash

# Update navigation for units 23-30 that have the different structure

for i in {23..30}; do
    file="/workspaces/Curriculum/units/unit${i}.html"
    
    if [ -f "$file" ]; then
        echo "Updating unit${i}.html..."
        
        # Get the unit title
        title=$(grep -o '<h1>Unit [^<]*</h1>' "$file" | sed 's/<[^>]*>//g')
        subtitle=$(grep -A1 '<h1>Unit' "$file" | grep '<p>' | sed 's/<[^>]*>//g' | xargs)
        
        # Create navigation elements
        prev=$((i-1))
        next=$((i+1))
        
        if [ $i -eq 30 ]; then
            next_link="<a href=\"unit${next}.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px; font-size: 0.9em;\">Next ➡</a>"
        else
            next_link="<a href=\"unit${next}.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px; font-size: 0.9em;\">Next ➡</a>"
        fi
        
        # Replace the header section
        sed -i '/        <div class="header">/,/        <\/div>/{
            /        <div class="header">/r /dev/stdin
            d
        }' "$file" << EOF
        <div class="header">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <a href="../curriculum-main.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 0.9em;">🏠 Back to Overview</a>
                <div style="display: flex; gap: 15px;">
                    <a href="index.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px; font-size: 0.9em;">📚 All Units</a>
                    <a href="unit${prev}.html" style="color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px; font-size: 0.9em;">⬅ Previous</a>
                    ${next_link}
                </div>
            </div>
            ${title}
            <p>${subtitle}</p>
        </div>
EOF
        
        echo "✓ Updated unit${i}.html"
    else
        echo "✗ File unit${i}.html not found"
    fi
done

echo "Navigation update complete for units 23-30!"
