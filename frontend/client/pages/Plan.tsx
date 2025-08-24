import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";
import { ArrowLeft, RefreshCw, Play, Calendar, Target, Users } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Plan() {
  const navigate = useNavigate();

  // Mock plan data - in real app this would come from API/state
  const mockPlan = {
    title: "Digital Marketing Strategy for Q1 2024",
    category: "Marketing",
    phases: [
      {
        title: "Research & Analysis",
        duration: "2 weeks",
        tasks: [
          "Conduct competitor analysis",
          "Analyze target audience demographics",
          "Review current brand positioning",
          "Identify key performance indicators"
        ]
      },
      {
        title: "Strategy Development",
        duration: "1 week", 
        tasks: [
          "Define brand messaging framework",
          "Create content strategy outline",
          "Develop channel distribution plan",
          "Set campaign objectives and budgets"
        ]
      },
      {
        title: "Implementation",
        duration: "4 weeks",
        tasks: [
          "Launch social media campaigns",
          "Execute content marketing plan",
          "Implement SEO optimization",
          "Monitor and adjust tactics"
        ]
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="outline"
            onClick={() => navigate("/dashboard")}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
          
          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Generated Strategy Plan
              </h1>
              <div className="flex items-center gap-2">
                <Badge variant="secondary">{mockPlan.category}</Badge>
                <span className="text-gray-600">•</span>
                <span className="text-gray-600">Generated just now</span>
              </div>
            </div>
            
            <div className="flex gap-2">
              <Button variant="outline">
                <RefreshCw className="h-4 w-4 mr-2" />
                Regenerate Plan
              </Button>
              <Button className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                <Play className="h-4 w-4 mr-2" />
                Execute Plan
              </Button>
            </div>
          </div>
        </div>

        {/* Plan Overview */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5 text-purple-600" />
              {mockPlan.title}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-3 gap-4 text-center">
              <div className="p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">3</div>
                <div className="text-sm text-gray-600">Phases</div>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">7</div>
                <div className="text-sm text-gray-600">Weeks Duration</div>
              </div>
              <div className="p-4 bg-indigo-50 rounded-lg">
                <div className="text-2xl font-bold text-indigo-600">12</div>
                <div className="text-sm text-gray-600">Total Tasks</div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Plan Phases */}
        <div className="space-y-6">
          {mockPlan.phases.map((phase, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="bg-gradient-to-r from-purple-600 to-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">
                      {index + 1}
                    </span>
                    {phase.title}
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <Calendar className="h-4 w-4" />
                    {phase.duration}
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {phase.tasks.map((task, taskIndex) => (
                    <li key={taskIndex} className="flex items-center gap-3">
                      <div className="w-2 h-2 bg-purple-400 rounded-full"></div>
                      <span className="text-gray-700">{task}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Action Section */}
        <Card className="mt-8 bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
          <CardContent className="p-6 text-center">
            <div className="space-y-4">
              <div className="flex items-center justify-center gap-2 text-purple-600">
                <Users className="h-5 w-5" />
                <span className="font-semibold">Ready to execute this plan?</span>
              </div>
              <p className="text-gray-600">
                Take your strategy to the next level with our execution tools and team collaboration features.
              </p>
              <Button 
                size="lg"
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                onClick={() => navigate("/execute")}
              >
                <Play className="h-4 w-4 mr-2" />
                Start Execution
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
