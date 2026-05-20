# ChatGPT — Booking Workflow

## Topics Covered
- Appointment request flow
- Booking statuses
- Doctor approval system
- Pending/confirmed/cancelled logic

## Example Prompts

### Prompt
The patient should request appointment first and doctor should accept it.

### Response Summary
- Added pending status
- Added accept/reject buttons
- Added update_booking_status view

---

### Prompt
Why is booking showing confirmed before doctor approval?

### Response Summary
- Booking status initialized incorrectly
- Fixed by setting status='pending'

---

### Prompt
After doctor approval patient should get email and dashboard update.

### Response Summary
- Send email after confirmation
- Update booking status
- Refresh dashboards