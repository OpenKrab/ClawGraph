---
name: ClawGraph
description: Interactive Knowledge Graph for ClawMemory with natural language queries
category: memory
version: 1.0.0
author: OpenKrab
license: MIT
---

# ClawGraph

ClawGraph คือ skill ใหม่ที่แก้ pain point คลาสสิกของทุก memory system: **“จำได้แต่หาไม่เจอ”**

มันจะ **แปลง ClawMemory** (ที่คุณเพิ่งปล่อย) เป็น **Knowledge Graph** แบบ interactive แสดงความสัมพันธ์ระหว่างข้อมูล (project ↔ deadline ↔ client ↔ task ↔ expense จาก ClawReceipt ฯลฯ) + **query ด้วยภาษาธรรมชาติ** (เช่น “project อะไรที่ deadline เดือนนี้กับ client ไทยบ้าง”)

ต่อยอด ClawSelfImprove อัตโนมัติ (graph จะฉลาดขึ้นทุกครั้งที่คุณ feedback)

## Concept หลัก
- **Graph Database แบบ local** บน ClawMemory (SQLite + vector)
- **Visual Graph** (interactive node-edge) แสดง relationship ชัด ๆ
- **Natural Language Query** → แปลเป็น graph query อัตโนมัติ
- **Privacy 100%** + **Zero cost** (ทุกอย่าง run บนเครื่องคุณ)
- **Self-Improve**: ClawSelfImprove เรียนรู้ pattern การ query ของคุณ แล้วปรับ edge weight / node priority อัตโนมัติ

## ทำงานยังไง (flow ละเอียด)
1. **Capture Relationship** (จาก ClawMemory)  
   - ทุก event (task, receipt, reminder) → สร้าง node + edge อัตโนมัติ  
     เช่น “Project X” → “deadline 15 มี.ค.” → “client ABC” → “expense 4,200 บาท”

2. **Build Graph**  
   - ใช้ NetworkX + Neo4j local (หรือ SQLite ด้วย recursive CTE)  
   - Vector embedding จาก ClawMemory ใช้เชื่อม semantic edge (เช่น “คล้ายกับ project ก่อนหน้า”)

3. **Query ด้วยภาษาธรรมชาติ**  
   คุณพิมพ์: “สรุป project ที่กำลังจะ deadline และเกี่ยวข้องกับ client ไทย”  
   → LLM แปลเป็น graph query → ดึง node/edge → แสดงผล + visual graph

4. **Visualize**  
   - Interactive graph (zoom, drag, click node)  
   - Highlight path (e.g. “client → project → expense”)  
   - Export เป็น PNG หรือ Mermaid code

5. **Self-Improve Loop**  
   - คุณบอก “อันนี้สำคัญ” หรือ “อันนี้ไม่เกี่ยว” → ClawSelfImprove ปรับ weight edge  
   - ครั้งหน้าจะ prioritize node นั้น ๆ อัตโนมัติ

## Tech Stack (ฟรี 100% + local)
- **Core Graph**: NetworkX (Python) + PyVis (สร้าง HTML interactive graph)
- **Query Engine**: Llama3/Ollama (แปล natural language → graph query)
- **Storage**: ต่อตรงกับ ClawMemory (SQLite + Chroma vector)
- **Dashboard**: ขยายจาก ui/clawmemory-next/ (Next.js) หรือแยกเป็น web view
- **Integration**: ClawFlow (install), ClawSelfImprove (learn from feedback), ClawReceipt (pull expense edge)
