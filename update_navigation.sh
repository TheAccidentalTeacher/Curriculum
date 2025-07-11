#!/bin/bash

# Script to add navigation to all unit files

for i in {4..32}; do
    file="/workspaces/Curriculum/units/unit${i}.html"
    
    if [ -f "$file" ]; then
        echo "Updating unit${i}.html..."
        
        # Determine previous and next unit numbers
        prev=$((i-1))
        next=$((i+1))
        
        # Build navigation elements
        prev_link="<a href=\"unit${prev}.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px;\">⬅ Previous</a>"
        
        if [ $i -eq 32 ]; then
            next_link="<span style=\"color: rgba(255,255,255,0.5); padding: 8px 16px;\">Next ➡</span>"
        else
            next_link="<a href=\"unit${next}.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.3); padding: 8px 16px; border-radius: 20px;\">Next ➡</a>"
        fi
        
        # Get the unit title
        title=$(grep -o '<h1>Unit [^<]*</h1>' "$file" | sed 's/<[^>]*>//g')
        
        # Create new navigation section
        new_nav="    <header>
        <h1>${title}</h1>
        <nav style=\"display: flex; justify-content: space-between; align-items: center; margin-top: 15px;\">
            <a href=\"../curriculum-main.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;\">🏠 Back to Overview</a>
            <div style=\"display: flex; gap: 15px;\">
                <a href=\"index.html\" style=\"color: white; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 20px;\">📚 All Units</a>
                ${prev_link}
                ${next_link}
            </div>
        </nav>
    </header>"
        
        # Replace the old header section
        sed -i '/<header>/,/<\/header>/c\
'"$new_nav" "$file"
        
        echo "Updated unit${i}.html"
    else
        echo "File unit${i}.html not found"
    fi
done

echo "Navigation update complete!"
