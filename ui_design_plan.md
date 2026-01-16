# UI Design Plan - TIF Compressor

This document outlines the UI component architecture for the TIF Compressor application, following the Firefox Design Specification (Mozilla Dot Design).

## 1. Color Palette Mapping
Based on the Firefox brand palette, we will use a "Dark Mode" or "High Contrast" approach suitable for a utility tool.

| Element | Category | Hex Value | Usage |
|---------|----------|-----------|-------|
| **Background (Main)** | Dark Blue | `#0A214D` | Main window background |
| **Background (Surface)** | Darker Blue | `#073072` | Frames, Job List background |
| **Primary Action** | Blue | `#0060E0` | "Start Compression" button |
| **Secondary Action** | Teal | `#068989` | "Add Files", "Add Folder" buttons |
| **Text (Primary)** | White | `#FFFFFF` | Headings, main labels |
| **Text (Secondary)** | Light Teal | `#B3FFE3` | Sub-labels, path hints |
| **Success Signal** | Green | `#3FE1B0` | Completed job indicator, progress bar |
| **Error Signal** | Red | `#FF505F` | Failed job indicator, error messages |
| **Warning Signal** | Orange | `#FF7139` | Low disk space, overwrite warnings |

## 2. Typography Hierarchy
We will use `Metropolis` for structural headings and `Inter` for functional UI text.

| Level | Font Family | Size | Weight | Usage |
|-------|-------------|------|--------|-------|
| **Title** | Metropolis | 24px | Bold | App Header |
| **Section Header** | Metropolis | 16px | SemiBold | "Job Queue", "Settings" |
| **Body MD** | Inter | 14px | Regular | List items, button text |
| **Body SM** | Inter | 12px | Regular | File paths, status bar |
| **Caption** | Inter | 10px | Medium | Version info, legal |

*Note: Tkinter font sizes are often in points. 1px ≈ 0.75pt. We will adjust accordingly in implementation.*

## 3. Grid & Spacing
A strict 8px grid system will be used for all layout components.

- **Outer Padding**: 24px (3 units) around the main window.
- **Component Spacing**: 16px (2 units) between major sections.
- **Internal Padding**: 8px (1 unit) inside buttons and list items.
- **Alignment**: All elements left-aligned unless they are primary actions (right-aligned).

## 4. Component Architecture
The GUI will be refactored into a modular structure:

### A. Header (`HeaderFrame`)
- **Logo**: Placeholder for Firefox-style geometric icon.
- **Title**: "TIF Compressor" in Metropolis Bold.
- **Visual**: A subtle gradient line (Blue to Teal) at the bottom.

### B. File Selection Area (`SelectionFrame`)
- **Buttons**: "Add Files", "Add Folder" (Teal).
- **Output Path**: A read-only entry or label showing the selected destination.
- **Action**: "Select Output" button.

### C. Job List (`QueueFrame`)
- **Listbox/Treeview**: Styled with `#073072` background.
- **Scrollbar**: Custom styled to match the dark theme.
- **Empty State**: "Drag and drop files or use the buttons above" text.

### D. Action Bar (`FooterFrame`)
- **Progress Bar**: Green (`#3FE1B0`) on Dark Blue background.
- **Status Label**: "Ready", "Processing...", "Done".
- **Buttons**: "Cancel" (Outline/Red), "Start" (Solid Blue).

## 5. Visual Elements (Mozilla Dot Design)
- **Geometric Shapes**: Use rounded corners (8px radius) for buttons and frames to mimic the "Open" and "Kind" personality.
- **Dots**: Incorporate a small "dot" pattern or a single decorative dot next to headings to align with the "Mozilla Dot Design" motif.
- **Gradients**: Use a Blue-to-Purple gradient for the progress bar or header background to add depth.

## 6. Implementation Strategy
1.  **Theme Class**: Create a `Theme` class in `gui.py` to store all hex codes and font configurations.
2.  **Custom Styles**: Use `ttk.Style` to override default widget appearances.
3.  **Refactor `App`**: Break down `create_widgets` into the component methods defined above.
