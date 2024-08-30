# Changelog

## [0.1.0] - 2024-08-29

### Added

- **Created `CerebroDBManager` class** for managing tasks, reports, and attachments in the Cerebro system.
- **Implemented `add_report` method** for adding reports to tasks with comments, time spent, and optional attachments.
- **Added `Attachment` class** for handling file attachments with validation for thumbnails (supports JPG and PNG formats).
- **Implemented `_create_report_message` method** for creating a report message with a comment and duration in the task.
- **Implemented `_add_attachment` method** for attaching files and thumbnails to a report message.
- **Created `_add_attachments` method** to handle multiple attachments to a single report message.

### Features

- **Type hinting** throughout the code for better readability and maintenance.
- **Exception handling** to ensure reliability, including validation for file paths, thumbnail formats, and image dimensions.
- **Thumbnail validation**: Automatically validates that thumbnails are in JPG/PNG format and resized to 512x512 pixels.
- **Logging**: Integrated logging for warnings and error tracking, ensuring smooth debugging.
  
### Technical Details

- **The tool uses the Cerebro API** to interact with tasks, messages, and attachments in the Cerebro database.
- **Pillow (PIL)** is used for image validation and processing of thumbnails.
- **Modular design**: The `Attachment` and `CerebroDBManager` classes are designed to be used independently or in conjunction.

### Classes

- **Attachment**: Handles file paths, thumbnails, and descriptions for task attachments.
- **CerebroDBManager**: Manages connection to the Cerebro database, handles task reporting, and attachment management.

### Methods

- **`add_report`**: Adds a report to a task with optional attachments.
- **`_create_report_message`**: Internal method to create a report message for a task.
- **`_add_attachment`**: Adds a single attachment to a message.
- **`_add_attachments`**: Adds multiple attachments to a report message.