import { NextRequest, NextResponse } from 'next/server'
import { exec } from 'child_process'
import { join } from 'path'
import { promisify } from 'util'
import { writeFile } from 'fs/promises'

const execAsync = promisify(exec)

export async function POST(request: NextRequest) {
  try {
    const { analysisType } = await request.json()
    
    if (!analysisType) {
      return NextResponse.json({ 
        error: 'Analysis type is required' 
      }, { status: 400 })
    }

    // Path to the parent directory where Python scripts are located
    const pythonDir = join(process.cwd(), '..')
    
    // Create analysis prompts based on type
    let analysisPrompt = ''
    switch (analysisType) {
      case 'skills':
        analysisPrompt = 'Analyze the person\'s technical and soft skills. Provide a comprehensive breakdown of their competencies, skill levels, and areas for improvement.'
        break
      case 'experience':
        analysisPrompt = 'Analyze the person\'s work experience and career progression. Identify patterns, growth areas, and career trajectory insights.'
        break
      case 'education':
        analysisPrompt = 'Analyze the person\'s educational background and how it relates to their career. Assess the relevance and impact of their education.'
        break
      case 'overall':
      default:
        analysisPrompt = 'Provide a comprehensive professional analysis of this person including strengths, weaknesses, career potential, and recommendations for growth.'
        break
    }        // Write a temporary Python script file    const scriptPath = join(pythonDir, 'temp_general_analyze.py')    const scriptContent = `import sysimport ossys.path.append('${pythonDir.replace(/\\/g, '/')}')try:    from llama_client import LlamaProcessor    import json        processor = LlamaProcessor()    person_data = processor.load_person_data()    if not person_data:        print("ERROR: No person data found")        sys.exit(1)    # Handle list format from CrustData API    if isinstance(person_data, list) and len(person_data) > 0:        person = person_data[0]    else:        person = person_data    # Create analysis prompt    prompt = f"""    Based on the following person's profile:    {json.dumps(person, indent=2)}    ${analysisPrompt}    Please provide detailed insights, specific examples from their profile, and actionable recommendations.    """    # Get response    completion = processor.client.chat.completions.create(
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
      const { stdout, stderr } = await execAsync(`python3 temp_general_analyze.py`, {
        cwd: pythonDir,
        timeout: 30000
      })
      
      // Clean up temp file
      await execAsync(`rm temp_general_analyze.py`, { cwd: pythonDir })
      
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
        await execAsync(`rm temp_general_analyze.py`, { cwd: pythonDir })
      } catch {}
      
      console.error('Execution error:', execError)
      return NextResponse.json({ 
        success: false,
        error: 'Failed to execute analysis script' 
      }, { status: 500 })
    }

  } catch (error) {
    console.error('General analysis API error:', error)
    return NextResponse.json({ 
      success: false,
      error: 'Internal server error' 
    }, { status: 500 })
  }
}
