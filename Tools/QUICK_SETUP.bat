@echo off
REM ========================================
REM QUICK COPY TO CLAUDE.MD - VERSION A
REM ========================================
REM This script copies all tools directly to C:\Users\aztec\CLAUDE.MD\Tools\Version_A
REM No need to run PowerShell - just double-click this file!

echo.
echo ========================================
echo CLAUDE.MD TOOLS - VERSION A SETUP
echo ========================================
echo.
echo This will copy all tools to:
echo C:\Users\aztec\CLAUDE.MD\Tools\Version_A
echo.
pause

REM Create base directory
if not exist "C:\Users\aztec\CLAUDE.MD\Tools" mkdir "C:\Users\aztec\CLAUDE.MD\Tools"

REM Create Version_A structure
echo Creating folder structure...
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active\Agent_Creator" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active\Agent_Migration_Enforcer" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active\Perplexity_Researcher" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending\Writer" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending\Mapper" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending\Research" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\LangGraph_RAG" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\Autogen_MultiAgent" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\Agno_Specialists" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\CrewAI_Workflows" 2>nul
mkdir "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation" 2>nul

echo Copying Active Tools...
xcopy /Y /Q "Agent_Creator\*" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active\Agent_Creator\"
xcopy /Y /Q "Agent_Migration_Enforcer\*" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active\Agent_Migration_Enforcer\"
xcopy /Y /Q "Perplexity_Researcher\*" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Active\Perplexity_Researcher\"

echo Copying Pending Tools (migration guides)...
xcopy /Y /Q "Writer\README.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending\Writer\"
xcopy /Y /Q "Mapper\README.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending\Mapper\"
xcopy /Y /Q "Research\README.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Pending\Research\"

echo Copying Documentation...
xcopy /Y /Q "CLAUDE.MD" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "MIGRATION_GUIDE.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "TOOLS_INDEX.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "README.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "QUICK_START.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "SYSTEM_STATUS.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "SUMMARY.txt" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"
xcopy /Y /Q "AGENT_CREATOR_V2_COMPLETE.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Documentation\"

echo Copying Useful Tools documentation...
xcopy /Y /Q "USEFUL_TOOLS_LANGGRAPH_RAG.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\LangGraph_RAG\"
xcopy /Y /Q "USEFUL_TOOLS_AUTOGEN.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\Autogen_MultiAgent\"
xcopy /Y /Q "USEFUL_TOOLS_AGNO.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\Agno_Specialists\"
xcopy /Y /Q "USEFUL_TOOLS_CREWAI.md" "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\Useful_From_500AI\CrewAI_Workflows\"

echo Creating manifests...
(
echo # VERSION A MANIFEST
echo Created: %date% %time%
echo Location: C:\Users\aztec\CLAUDE.MD\Tools\Version_A
echo.
echo Contents:
echo - 3 Active Tools
echo - 3 Pending Tools ^(migration guides^)
echo - 26+ Useful Tools ^(documented^)
echo - 8 Documentation files
echo.
echo See Documentation\CLAUDE.MD for complete catalog
) > "C:\Users\aztec\CLAUDE.MD\Tools\Version_A\VERSION_A_MANIFEST.txt"

(
echo # MASTER INDEX
echo All NACFE Tools organized by version
echo.
echo Current Version: A
echo Location: C:\Users\aztec\CLAUDE.MD\Tools\Version_A
echo.
echo See VERSION_A_MANIFEST.txt for details
) > "C:\Users\aztec\CLAUDE.MD\Tools\MASTER_INDEX.txt"

echo.
echo ========================================
echo SUCCESS! Version A installed at:
echo C:\Users\aztec\CLAUDE.MD\Tools\Version_A
echo ========================================
echo.
echo Next steps:
echo 1. Open: C:\Users\aztec\CLAUDE.MD\Tools\Version_A
echo 2. Read: VERSION_A_MANIFEST.txt
echo 3. Use tools from: Active\ folder
echo.
pause

explorer "C:\Users\aztec\CLAUDE.MD\Tools\Version_A"
