const htmlContent = document.documentElement.outerHTML;

let filename = 'page.html';
const titleContainer = document.querySelector('.document-title.text-2xl-md-lh');
if (titleContainer) {
const titleSpan = titleContainer.querySelector('span');
if (titleSpan) {
    filename = titleSpan.textContent
	.trim()
	.replace(/[<>:"/\\|?*]+/g, '-')
	.replace(/\s+/g, '_')          
	.toLowerCase() + '.html';
}
}

const blob = new Blob([htmlContent], { type: 'text/html' });

const link = document.createElement('a');
link.href = URL.createObjectURL(blob);
link.download = filename;

document.body.appendChild(link);
link.click();
document.body.removeChild(link);

URL.revokeObjectURL(link.href);

console.log(`Saved as: ${filename}`);
