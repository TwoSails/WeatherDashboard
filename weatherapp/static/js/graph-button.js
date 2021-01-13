function toggle_visibility(id) {
            const idList = ['windDirection-chart-area', 'avgWindSpeed-chart-area', 'windGust-chart-area', 'rainfall-chart-area', 'humidity-chart-area', 'ambient-chart-area'];
            for (x of idList) {
                const doc = document.getElementById(x);
                const style = getComputedStyle(doc);
                if (style.display === 'flex' && x !== id) {
                    doc.style.display = 'none';
                }
            }
            const doc = document.getElementById(id);
            const style = getComputedStyle(doc);
            if (style.display === 'none') {
            doc.style.display = 'flex';
        } else {
                doc.style.display = 'none';
            }

   }