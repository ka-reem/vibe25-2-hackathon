import { NextRequest, NextResponse } from 'next/server'
import { exec } from 'child_process'
import { join } from 'path'
import { promisify } from 'util'
import { writeFile } from 'fs/promises'

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const { jobDescription } = await request.json()
    
    if (!jobDescription || !jobDescription.trim()) {
      return NextResponse.json({ 
        error: 'Job description is required' 
      }, { status: 400 })
    }

    // Path to the parent directory where Python scripts are located
    const pythonDir = join(process.cwd(), '..')
    
    // Escape the job description for Python
    const escapedJobDesc = jobDescription.replace(/"/g, '\\"').replace(/\n/g, '\\n')
    
    // Write a temporary Python script file
    const scriptPath = join(pythonDir, 'temp_analyze.py')
    const scriptContent = `import sys
import os
sys.path.append('${pythonDir.replace(/\\/g, '/')}')

try:
    from llama_client import LlamaProcessor
    import json
    
    processor = LlamaProcessor()
    person_data = processor.load_person_data()

    if not person_data:
        print("ERROR: No person data found")
        sys.exit(1)

    # Handle list format from CrustData API
    if isinstance(person_data, list) and len(person_data) > 0:
        person = person_data[0]
    else:
        person = person_data

    # Create job analysis prompt
    job_desc = "${escapedJobDesc}"
    
    prompt = f"""Based on the following person's profile, analyze their fit for this job:

Person Profile:
{json.dumps(person, indent=2)}

Job Description:
{job_desc}

Please provide:
1. Overall fit score (1-10)
2. Key strengths that match the role
3. Potential gaps or areas for development
4. Specific recommendations
5. Skills alignment analysis

Format your response in a clear, professional manner."""

    # Get response
    completion = processor.client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",
        messages=[{"role": "user", "content": prompt}],
    )
    
    response = completion.choices[0].message.content
    print("SUCCESS:" + response)
    
except Exception as e:
    print("ERROR:" + str(e))
`

    await writeFile(scriptPath, scriptContent)
    
    try {
      const { stdout, stderr } = await execAsync(`python3 temp_analyze.py`, {
        cwd: pythonDir,
        timeout: 30000
      })
      
      // Clean up temp file
      await execAsync(`rm temp_analyze.py`, { cwd: pythonDir })
      
      if (stdout.startsWith('SUCCESS:')) {
        const response = stdout.substring(8).trim()
        return NextResponse.json({ 
          success: true, 
          analysis: response 
        })
      } else if (stdout.startsWith('ERROR:')) {
        const error = stdout.substring(6).trim()
        return NextResponse.json({ 
          success: false,
          error 
        }, { status: 500 })
      } else {
        return NextResponse.json({ 
          success: false,
          error: `Unexpected output: ${stderr || 'Unknown error'}` 
        }, { status: 500 })
      }
    } catch (execError: unknown) {
      // Clean up temp file on error
      try {
        await execAsync(`rm temp_analyze.py`, { cwd: pythonDir })
      } catch {}
      
      console.error('Execution error:', execError)
      return NextResponse.json({ 
        success: false,
        error: 'Failed to execute analysis script' 
      }, { status: 500 })
    }

  } catch (error) {
    console.error('Analyze job API error:', error)
    return NextResponse.json({ 
      success: false,
      error: 'Internal server error' 
    }, { status: 500 })
  }
}
