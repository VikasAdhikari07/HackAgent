import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Header from "@/components/Header";
import { ArrowLeft, ExternalLink, Calendar, CheckCircle, Clock } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Execute() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="outline"
            onClick={() => navigate("/plan")}
            className="mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Plan
          </Button>
          
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Execute Your Strategy
          </h1>
          <p className="text-gray-600">
            Choose how you'd like to execute your strategy plan and track progress.
          </p>
        </div>

        {/* Execution Options */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card className="border-2 border-purple-200 hover:border-purple-400 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-purple-600" />
                Project Management Integration
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Export your plan to popular project management tools like Asana, Trello, or Monday.com.
              </p>
              <Button className="w-full" variant="outline">
                <ExternalLink className="h-4 w-4 mr-2" />
                Connect Tools
              </Button>
            </CardContent>
          </Card>

          <Card className="border-2 border-blue-200 hover:border-blue-400 transition-colors cursor-pointer">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="h-5 w-5 text-blue-600" />
                Built-in Task Tracker
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 mb-4">
                Use our integrated task management system to track progress and collaborate with your team.
              </p>
              <Button className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700">
                Start Tracking
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Coming Soon Features */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-indigo-600" />
              Coming Soon
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-indigo-400 rounded-full"></div>
                <span className="text-gray-700">AI-powered progress monitoring</span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-indigo-400 rounded-full"></div>
                <span className="text-gray-700">Automated team notifications</span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-indigo-400 rounded-full"></div>
                <span className="text-gray-700">Performance analytics dashboard</span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="w-2 h-2 bg-indigo-400 rounded-full"></div>
                <span className="text-gray-700">Integration with CRM systems</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Call to Action */}
        <Card className="mt-8 bg-gradient-to-r from-purple-50 to-blue-50 border-purple-200">
          <CardContent className="p-6 text-center">
            <div className="space-y-4">
              <h3 className="text-xl font-semibold text-gray-900">
                Ready to Turn Plans into Results?
              </h3>
              <p className="text-gray-600">
                Our execution tools are currently in development. Join our waitlist to be the first to access these powerful features.
              </p>
              <Button 
                size="lg"
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
              >
                Join Waitlist
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
